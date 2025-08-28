# path_traversal_demo.py
import os
import sys
from pathlib import Path

class FileServer:
    def __init__(self, web_root="./web_files"):
        self.web_root = os.path.abspath(web_root)
        self.setup_demo_files()
    
    def setup_demo_files(self):
        """Create demo file structure"""
        os.makedirs(self.web_root, exist_ok=True)
        os.makedirs(f"{self.web_root}/public", exist_ok=True)
        os.makedirs(f"{self.web_root}/private", exist_ok=True)
        
        # Public files
        with open(f"{self.web_root}/public/welcome.txt", 'w') as f:
            f.write("Welcome to our public website!\nThis file is safe to access.")
        
        with open(f"{self.web_root}/public/info.html", 'w') as f:
            f.write("<html><body><h1>Public Information</h1><p>This is publicly accessible.</p></body></html>")
        
        # Private/sensitive files
        with open(f"{self.web_root}/private/admin_passwords.txt", 'w') as f:
            f.write("ADMIN PASSWORDS - CONFIDENTIAL\n")
            f.write("admin:super_secret_password_123\n")
            f.write("root:another_secret_pass_456\n")
            f.write("database:db_admin_pass_789\n")
        
        with open(f"{self.web_root}/config.ini", 'w') as f:
            f.write("[DATABASE]\n")
            f.write("host=internal-db-server\n")
            f.write("username=db_user\n")
            f.write("password=secret_db_password_xyz\n")
            f.write("[API_KEYS]\n")
            f.write("stripe_secret=sk_live_51AbCdEf...\n")
            f.write("aws_secret=wJalrXUtnFEMI/K7MDENG...\n")
        
        # System files simulation
        os.makedirs("/tmp/demo_system", exist_ok=True)
        with open("/tmp/demo_system/shadow", 'w') as f:
            f.write("root:$6$randomsalt$hashedpassword:18000:0:99999:7:::\n")
            f.write("admin:$6$anothersalt$hashedpassword:18000:0:99999:7:::\n")
    
    def vulnerable_read_file(self, filename):
        """VULNERABLE - Direct path concatenation allows traversal"""
        try:
            file_path = os.path.join(self.web_root, "public", filename)
            print(f"🔍 Attempting to read: {file_path}")
            
            # Vulnerable: No path validation
            with open(file_path, 'r') as f:
                content = f.read()
                return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def safe_read_file(self, filename):
        """SAFE - Proper path validation and sandboxing"""
        try:
            # Resolve the full path
            requested_path = os.path.join(self.web_root, "public", filename)
            resolved_path = os.path.abspath(requested_path)
            
            print(f"🔍 Requested: {filename}")
            print(f"🔍 Resolved path: {resolved_path}")
            print(f"🔍 Web root: {self.web_root}")
            
            # Security check: Ensure the resolved path is within web root
            if not resolved_path.startswith(os.path.join(self.web_root, "public")):
                return "🚫 Access denied: Path traversal attempt detected!"
            
            # Additional check: No parent directory references
            if ".." in filename or filename.startswith("/"):
                return "🚫 Access denied: Invalid path characters detected!"
            
            with open(resolved_path, 'r') as f:
                content = f.read()
                return content
                
        except FileNotFoundError:
            return "❌ File not found in public directory"
        except Exception as e:
            return f"❌ Error: {str(e)}"

def demonstrate_path_traversal():
    print("=== Path Traversal Vulnerability Demonstration ===\n")
    
    server = FileServer()
    
    print("📁 File structure created:")
    print("  web_files/")
    print("  ├── public/")
    print("  │   ├── welcome.txt (✅ Safe to access)")
    print("  │   └── info.html (✅ Safe to access)")
    print("  ├── private/")
    print("  │   └── admin_passwords.txt (🔒 Should be protected)")
    print("  └── config.ini (🔒 Should be protected)")
    print()
    print("=" * 70)
    print()
    
    # Test cases
    test_cases = [
        ("welcome.txt", "Normal file access"),
        ("../config.ini", "Access parent directory config"),
        ("../private/admin_passwords.txt", "Access private admin passwords"),
        ("../../../../../../tmp/demo_system/shadow", "Access system files"),
        ("../private/../config.ini", "Complex traversal attempt"),
        ("%2e%2e%2fconfig.ini", "URL encoded traversal"),
    ]
    
    print("🚨 VULNERABLE VERSION - Testing Path Traversal:")
    print("-" * 50)
    
    for filename, description in test_cases:
        print(f"\n📋 Test: {description}")
        print(f"📝 Input: '{filename}'")
        result = server.vulnerable_read_file(filename)
        
        # Truncate long results for readability
        if len(result) > 200:
            print(f"📄 Result: {result[:200]}...")
        else:
            print(f"📄 Result: {result}")
        
        if "ADMIN PASSWORDS" in result or "DATABASE" in result or "root:" in result:
            print("⚠️  🚨 SECURITY BREACH: Sensitive data exposed! 🚨")
        
        print("-" * 50)
    
    print("\n" + "=" * 70)
    print("\n✅ SAFE VERSION - Testing with Protection:")
    print("-" * 40)
    
    for filename, description in test_cases[:4]:  # Test subset with safe version
        print(f"\n📋 Test: {description}")
        print(f"📝 Input: '{filename}'")
        result = server.safe_read_file(filename)
        print(f"📄 Result: {result}")
        print("-" * 40)

def demonstrate_url_encoding_bypass():
    """Additional demo showing URL encoding bypass attempts"""
    print("\n" + "=" * 70)
    print("🔧 ADVANCED: URL Encoding Bypass Attempts")
    print("-" * 40)
    
    server = FileServer()
    
    encoded_payloads = [
        ("%2e%2e%2fconfig.ini", "URL encoded ../"),
        ("%2e%2e%2f%2e%2e%2fconfig.ini", "Double URL encoded ../"),
        ("..%252fconfig.ini", "Double URL encoded /"),
        ("..%c0%afconfig.ini", "Unicode bypass attempt"),
    ]
    
    for payload, description in encoded_payloads:
        print(f"\n📋 Test: {description}")
        print(f"📝 Payload: '{payload}'")
        
        # Simulate URL decoding (in real webapp, this happens automatically)
        import urllib.parse
        decoded = urllib.parse.unquote(payload)
        print(f"📝 Decoded: '{decoded}'")
        
        result = server.vulnerable_read_file(decoded)
        if len(result) > 100:
            print(f"📄 Result: {result[:100]}...")
        else:
            print(f"📄 Result: {result}")
            
        print("-" * 40)

if __name__ == "__main__":
    demonstrate_path_traversal()
    demonstrate_url_encoding_bypass()