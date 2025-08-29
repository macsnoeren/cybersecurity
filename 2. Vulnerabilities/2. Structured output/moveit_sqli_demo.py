# moveit_sqli_demo.py - Educational simulation of CVE-2023-34362
import sqlite3
import sys
from urllib.parse import unquote

class MOVEitTransferSimulation:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.setup_database()
    
    def setup_database(self):
        """Simulate MOVEit Transfer database structure"""
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password_hash TEXT,
                email TEXT,
                role TEXT,
                last_login TEXT
            )
        ''')
        
        # Files table - contains sensitive data
        cursor.execute('''
            CREATE TABLE uploaded_files (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                upload_user TEXT,
                file_path TEXT,
                file_size INTEGER,
                upload_date TEXT,
                classification TEXT
            )
        ''')
        
        # Populate with realistic data
        users = [
            (1, 'admin', 'hash123', 'admin@company.com', 'administrator', '2023-05-27'),
            (2, 'hr_dept', 'hash456', 'hr@company.com', 'user', '2023-05-26'),
            (3, 'finance', 'hash789', 'finance@company.com', 'user', '2023-05-25'),
            (4, 'legal', 'hash999', 'legal@company.com', 'user', '2023-05-24')
        ]
        
        files = [
            (1, 'employee_salaries_2023.xlsx', 'hr_dept', '/uploads/hr/', 2048576, '2023-05-20', 'CONFIDENTIAL'),
            (2, 'financial_report_q1.pdf', 'finance', '/uploads/finance/', 1024000, '2023-05-21', 'RESTRICTED'),
            (3, 'customer_database.csv', 'admin', '/uploads/admin/', 5242880, '2023-05-22', 'CONFIDENTIAL'),
            (4, 'legal_contracts.zip', 'legal', '/uploads/legal/', 3145728, '2023-05-23', 'RESTRICTED'),
            (5, 'backup_user_credentials.txt', 'admin', '/uploads/system/', 512000, '2023-05-19', 'TOP_SECRET')
        ]
        
        cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', users)
        cursor.executemany('INSERT INTO uploaded_files VALUES (?, ?, ?, ?, ?, ?, ?)', files)
        self.conn.commit()
    
    def vulnerable_file_search(self, search_term, user_context='guest'):
        """VULNERABLE - Direct SQL concatenation (CVE-2023-34362 simulation)"""
        cursor = self.conn.cursor()
        
        # Decode URL encoding
        decoded_search = unquote(search_term)
        
        print(f"🔍 MOVEit: Searching for files containing: {search_term}")
        print(f"🔍 Decoded search term: {decoded_search}")
        
        # VULNERABLE: Direct string concatenation in SQL query
        # This mirrors the actual vulnerability in MOVEit Transfer
        query = f"""
        SELECT f.filename, f.upload_user, f.file_size, f.classification, u.email
        FROM uploaded_files f 
        JOIN users u ON f.upload_user = u.username 
        WHERE f.filename LIKE '%{decoded_search}%' 
        AND (f.classification != 'TOP_SECRET' OR u.username = '{user_context}')
        """
        
        print(f"🔍 Executing query: {query}")
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"❌ Database error: {e}")
            return []
    
    def safe_file_search(self, search_term, user_context='guest'):
        """SAFE - Parameterized query"""
        cursor = self.conn.cursor()
        
        # Input validation
        if len(search_term) > 100 or any(char in search_term for char in ['\'', '"', ';', '--']):
            return "❌ Invalid search term"
        
        # Parameterized query
        query = """
        SELECT f.filename, f.upload_user, f.file_size, f.classification, u.email
        FROM uploaded_files f 
        JOIN users u ON f.upload_user = u.username 
        WHERE f.filename LIKE ? 
        AND (f.classification != 'TOP_SECRET' OR u.username = ?)
        """
        
        print(f"🔍 Safe search for: {search_term}")
        cursor.execute(query, (f'%{search_term}%', user_context))
        return cursor.fetchall()

def demonstrate_moveit_sqli():
    print("=== MOVEit Transfer SQL Injection Simulation (CVE-2023-34362) ===")
    print("Real-world impact: CL0P ransomware gang stole data from 600+ organizations\n")
    
    moveit = MOVEitTransferSimulation()
    
    print("📊 Available files in MOVEit Transfer:")
    all_files = moveit.conn.execute("SELECT filename, classification FROM uploaded_files").fetchall()
    for filename, classification in all_files:
        print(f"  - {filename} ({classification})")
    print()
    
    print("=" * 80)
    print("🚨 VULNERABLE VERSION - SQL Injection Attack (CVE-2023-34362)")
    print("=" * 80)
    
    # Test 1: Normal search
    print("\n📋 Test 1: Normal file search")
    results = moveit.vulnerable_file_search("report")
    print(f"📄 Found {len(results)} files:")
    for result in results:
        print(f"  - {result[0]} ({result[3]}) - {result[1]}")
    
    # Test 2: SQL Injection - Authentication bypass and data extraction
    print("\n📋 Test 2: SQL Injection - Extract all files including TOP_SECRET")
    # This payload bypasses the TOP_SECRET restriction
    malicious_search = "' UNION SELECT filename, upload_user, file_size, classification, 'injected@attacker.com' FROM uploaded_files --"
    results = moveit.vulnerable_file_search(malicious_search)
    print(f"🚨 BREACH: Found {len(results)} files (including restricted):")
    for result in results:
        if result[3] == 'TOP_SECRET':
            print(f"  💀 STOLEN: {result[0]} ({result[3]}) - {result[1]}")
        else:
            print(f"  - {result[0]} ({result[3]}) - {result[1]}")
    
    # Test 3: Advanced SQL injection - Extract user credentials
    print("\n📋 Test 3: SQL Injection - Extract user credentials")
    credential_theft = "' UNION SELECT username, password_hash, email, role, last_login FROM users --"
    results = moveit.vulnerable_file_search(credential_theft)
    print("🚨 CREDENTIAL THEFT:")
    for result in results:
        print(f"  💀 User: {result[0]}, Hash: {result[1]}, Role: {result[3]}")
    
    # Test 4: Simulating webshell installation (LEMURLOOT)
    print("\n📋 Test 4: Webshell Installation Simulation")
    webshell_payload = "'; INSERT INTO uploaded_files (filename, upload_user, file_path, classification) VALUES ('human2.aspx', 'SYSTEM', '/web/', 'WEBSHELL') --"
    moveit.vulnerable_file_search(webshell_payload)
    
    # Check if webshell was installed
    webshells = moveit.conn.execute("SELECT filename, file_path FROM uploaded_files WHERE classification = 'WEBSHELL'").fetchall()
    if webshells:
        print("💀 WEBSHELL INSTALLED:")
        for shell in webshells:
            print(f"  🕷️  {shell[0]} at {shell[1]}")
            print("  🎯 Attacker now has persistent access to the server!")
    
    print("\n" + "=" * 80)
    print("✅ SAFE VERSION - Parameterized Queries")
    print("=" * 80)
    
    print("\n📋 Test 5: Safe search with same malicious input")
    safe_results = moveit.safe_file_search(malicious_search)
    print(f"✅ Safe search result: {safe_results}")
    
    print("\n📋 Test 6: Safe normal search")
    safe_results = moveit.safe_file_search("report")
    print(f"📄 Found {len(safe_results)} files safely:")
    for result in safe_results:
        print(f"  - {result[0]} ({result[3]})")

def show_real_world_timeline():
    print("\n" + "=" * 80)
    print("📅 REAL-WORLD ATTACK TIMELINE")
    print("=" * 80)
    print("May 27, 2023: CL0P gang begins exploiting CVE-2023-34362 as 0-day")
    print("May 31, 2023: Progress Software releases security advisory")
    print("June 2023:    Over 130 organizations confirmed breached")
    print("July 2023:    Victim count rises to 600+ organizations")
    print("Impact:       Millions of individuals' data stolen")
    print("Victims:      Government agencies, healthcare, corporations")
    print("Ransom:       CL0P demands payment to prevent data publication")

if __name__ == "__main__":
    demonstrate_moveit_sqli()
    show_real_world_timeline()