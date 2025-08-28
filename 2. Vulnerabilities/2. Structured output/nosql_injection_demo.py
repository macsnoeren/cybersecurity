# nosql_injection_demo.py
import json
import re
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import hashlib

class MockMongoDB:
    """Mock MongoDB for demonstration purposes"""
    def __init__(self):
        self.users = [
            {"username": "admin", "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "role": "administrator", "email": "admin@company.com"},
            {"username": "user1", "password": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f", "role": "user", "email": "user1@company.com"},
            {"username": "user2", "password": "secret123_hashed", "role": "user", "email": "user2@company.com"},
            {"username": "api_service", "password": "service_key_hash", "role": "service", "api_key": "sk_live_abc123xyz789"},
        ]
        self.products = [
            {"name": "Product A", "price": 99.99, "category": "electronics"},
            {"name": "Product B", "price": 49.99, "category": "books"},
            {"name": "Secret Product", "price": 0.01, "category": "internal", "internal_notes": "DO NOT SELL"},
        ]
    
    def find_user(self, query):
        """Simulate MongoDB find operation"""
        print(f"🔍 MongoDB Query: {json.dumps(query, indent=2)}")
        
        # Simple query simulation
        results = []
        for user in self.users:
            match = True
            for key, value in query.items():
                if key not in user:
                    match = False
                    break
                
                if isinstance(value, dict):
                    # Handle operators like $ne, $gt, etc.
                    for op, op_value in value.items():
                        if op == "$ne" and user[key] == op_value:
                            match = False
                        elif op == "$regex" and not re.search(op_value, str(user[key])):
                            match = False
                        elif op == "$exists" and (key in user) != op_value:
                            match = False
                else:
                    if user[key] != value:
                        match = False
                        break
            
            if match:
                results.append(user)
        
        return results
    
    def find_products(self, query):
        """Simulate MongoDB find operation for products"""
        print(f"🔍 MongoDB Query: {json.dumps(query, indent=2)}")
        
        results = []
        for product in self.products:
            match = True
            for key, value in query.items():
                if key not in product:
                    match = False
                    break
                
                if isinstance(value, dict):
                    for op, op_value in value.items():
                        if op == "$ne" and product[key] == op_value:
                            match = False
                        elif op == "$gt" and product[key] <= op_value:
                            match = False
                        elif op == "$regex" and not re.search(op_value, str(product[key])):
                            match = False
                elif product[key] != value:
                    match = False
                    break
            
            if match:
                results.append(product)
        
        return results

class UserAPI:
    def __init__(self):
        self.db = MockMongoDB()
    
    def vulnerable_login(self, username, password):
        """VULNERABLE - Direct JSON parsing allows injection"""
        try:
            # Parse JSON input directly into MongoDB query
            if isinstance(username, str) and isinstance(password, str):
                query = {"username": username, "password": password}
            else:
                # This is where the vulnerability lies - accepting complex objects
                query = {"username": username, "password": password}
            
            users = self.db.find_user(query)
            return len(users) > 0, users
            
        except Exception as e:
            return False, str(e)
    
    def safe_login(self, username, password):
        """SAFE - Input validation and sanitization"""
        try:
            # Input validation
            if not isinstance(username, str) or not isinstance(password, str):
                return False, "Invalid input types"
            
            if len(username) > 50 or len(password) > 100:
                return False, "Input too long"
            
            # Only allow alphanumeric characters and basic symbols in username
            if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
                return False, "Invalid username format"
            
            # Simple query with only string values
            query = {"username": username, "password": password}
            users = self.db.find_user(query)
            return len(users) > 0, users
            
        except Exception as e:
            return False, str(e)
    
    def vulnerable_search_products(self, filters):
        """VULNERABLE - Direct filter injection"""
        try:
            # Directly use user-provided filters in database query
            products = self.db.find_products(filters)
            return products
        except Exception as e:
            return str(e)
    
    def safe_search_products(self, filters):
        """SAFE - Whitelist approach for filters"""
        try:
            # Whitelist of allowed filter keys
            allowed_keys = ['name', 'price', 'category']
            safe_query = {}
            
            for key, value in filters.items():
                if key not in allowed_keys:
                    continue  # Skip disallowed keys
                
                # Only allow simple string/number values
                if isinstance(value, (str, int, float)):
                    safe_query[key] = value
                # Skip complex objects/operators
            
            products = self.db.find_products(safe_query)
            return products
        except Exception as e:
            return str(e)

def demonstrate_nosql_injection():
    print("=== NoSQL Injection Demonstration ===\n")
    
    api = UserAPI()
    
    print("👥 Available users in database:")
    all_users = api.db.find_user({})
    for user in all_users:
        print(f"  - {user['username']} ({user['role']})")
    print()
    
    print("🛍️ Available products:")
    all_products = api.db.find_products({})
    for product in all_products:
        print(f"  - {product['name']} (${product['price']}) - {product['category']}")
    print()
    
    print("=" * 70)
    print()
    
    print("🚨 VULNERABLE VERSION - NoSQL Injection Attacks:")
    print("-" * 50)
    
    # Test 1: Normal login
    print("\n📋 Test 1: Normal login attempt")
    success, result = api.vulnerable_login("user1", "wrong_password")
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    
    # Test 2: Authentication bypass using $ne operator
    print("\n📋 Test 2: Authentication bypass using $ne (not equal)")
    malicious_username = {"$ne": ""}  # Username not equal to empty string
    malicious_password = {"$ne": ""}  # Password not equal to empty string
    success, result = api.vulnerable_login(malicious_username, malicious_password)
    print(f"⚠️  Result: {'Success' if success else 'Failed'}")
    if success:
        print("🚨 SECURITY BREACH: Bypassed authentication without valid credentials!")
        print(f"🔓 Logged in as: {result[0]['username']} ({result[0]['role']})")
    
    # Test 3: Regex injection to extract user info
    print("\n📋 Test 3: Username enumeration using regex")
    username_pattern = {"$regex": "^admin"}  # Find users starting with "admin"
    password_bypass = {"$ne": ""}
    success, result = api.vulnerable_login(username_pattern, password_bypass)
    print(f"⚠️  Result: {'Success' if success else 'Failed'}")
    if success:
        print("🚨 USERNAME ENUMERATION: Found matching users!")
        for user in result:
            print(f"🔓 Found user: {user['username']}")
    
    # Test 4: Product injection - accessing internal data
    print("\n📋 Test 4: Product search - normal query")
    normal_filters = {"category": "electronics"}
    products = api.vulnerable_search_products(normal_filters)
    print(f"📦 Found {len(products)} products:")
    for p in products:
        print(f"  - {p['name']}")
    
    print("\n📋 Test 5: Product injection - accessing internal category")
    malicious_filters = {"category": {"$ne": "electronics"}}  # Get everything except electronics
    products = api.vulnerable_search_products(malicious_filters)
    print(f"📦 Found {len(products)} products:")
    for p in products:
        print(f"  - {p['name']} - {p.get('internal_notes', 'N/A')}")
        if 'internal_notes' in p:
            print("🚨 INTERNAL DATA EXPOSED!")
    
    # Test 6: Operator injection for data extraction
    print("\n📋 Test 6: Data extraction using $exists operator")
    api_key_search = {"api_key": {"$exists": True}}
    users = api.db.find_user(api_key_search)
    if users:
        print("🚨 API KEY EXPOSURE:")
        for user in users:
            print(f"  User: {user['username']}, API Key: {user.get('api_key', 'N/A')}")
    
    print("\n" + "=" * 70)
    print()
    
    print("✅ SAFE VERSION - Input Validation:")
    print("-" * 40)
    
    # Test safe login
    print("\n📋 Test 7: Safe login with object injection attempt")
    try:
        success, result = api.safe_login({"$ne": ""}, {"$ne": ""})
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"✅ Blocked: {str(e)}")
    
    print("\n📋 Test 8: Safe product search")
    safe_result = api.safe_search_products({"category": {"$ne": "electronics"}})
    print(f"📦 Safe search result: Found {len(safe_result)} products")
    for p in safe_result:
        print(f"  - {p['name']}")
    
    print("\n📋 Test 9: Safe login with valid credentials")
    success, result = api.safe_login("user1", "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f")
    print(f"✅ Result: {'Success' if success else 'Failed'}")

if __name__ == "__main__":
    demonstrate_nosql_injection()