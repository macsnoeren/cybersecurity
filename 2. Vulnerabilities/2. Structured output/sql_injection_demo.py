# sql_injection_demo.py
import sqlite3
import os

class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')  # In-memory database
        self.setup_database()
    
    def setup_database(self):
        """Create sample database with users"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                role TEXT,
                email TEXT
            )
        ''')
        
        # Insert sample data
        users = [
            (1, 'admin', 'admin123', 'administrator', 'admin@company.com'),
            (2, 'user1', 'password1', 'user', 'user1@company.com'),
            (3, 'user2', 'password2', 'user', 'user2@company.com'),
            (4, 'secretuser', 'topsecret', 'admin', 'secret@company.com')
        ]
        
        cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?)', users)
        self.conn.commit()
    
    def vulnerable_login(self, username, password):
        """VULNERABLE - Direct string concatenation"""
        cursor = self.conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing query: {query}")
        
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    def safe_login(self, username, password):
        """SAFE - Using parameterized queries"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        print(f"Executing safe query with parameters: username={username}, password={password}")
        
        cursor.execute(query, (username, password))
        result = cursor.fetchall()
        return result
    
    def show_all_users(self):
        """Display all users for demonstration"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, role, email FROM users")
        users = cursor.fetchall()
        print("All users in database:")
        for user in users:
            print(f"  ID: {user[0]}, Username: {user[1]}, Role: {user[2]}, Email: {user[3]}")

def demonstrate_sql_injection():
    print("=== SQL Injection Demonstration ===\n")
    
    db = UserDatabase()
    db.show_all_users()
    print("\n" + "="*50 + "\n")
    
    # Normal login
    print("Test 1: Normal login")
    result = db.vulnerable_login("user1", "password1")
    print(f"Login result: {result}\n")
    
    # SQL Injection Attack 1: Authentication bypass
    print("Test 2: SQL Injection - Authentication Bypass")
    malicious_input = "admin' OR '1'='1"
    result = db.vulnerable_login(malicious_input, "anything")
    print(f"Login result: {result}")
    print("⚠️  Successfully bypassed authentication!\n")
    
    # SQL Injection Attack 2: Union-based data extraction
    print("Test 3: SQL Injection - Data Extraction")
    malicious_input = "user1' UNION SELECT id, username, password, role, email FROM users --"
    result = db.vulnerable_login(malicious_input, "anything")
    print(f"Login result: {result}")
    print("⚠️  Successfully extracted all user data!\n")
    
    print("="*50 + "\n")
    
    # Safe version
    print("Test 4: Safe parameterized query")
    result = db.safe_login("admin' OR '1'='1", "anything")
    print(f"Safe login result: {result}")
    print("✅ Attack prevented by parameterized query!\n")

if __name__ == "__main__":
    demonstrate_sql_injection()