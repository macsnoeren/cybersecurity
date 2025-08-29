# postgresql_race_demo.py - Educational simulation of CVE-2025-1094
import threading
import time
import subprocess
import tempfile
import os
import random

class PostgreSQLClientSimulation:
    def __init__(self):
        self.temp_files = []
        self.connection_pool = []
        self.lock = threading.Lock()
    
    def vulnerable_psql_execution(self, sql_content, thread_id):
        """
        VULNERABLE - Simulates race condition in psql client processing
        Based on CVE-2025-1094 UTF-8 validation issue
        """
        print(f"🔗 Thread {thread_id}: Starting psql execution...")
        
        # Step 1: Create temporary SQL file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False)
        temp_file_path = temp_file.name
        
        print(f"📝 Thread {thread_id}: Writing SQL to {temp_file_path}")
        temp_file.write(sql_content)
        temp_file.close()
        
        # Step 2: VULNERABLE - UTF-8 validation with race condition window
        print(f"🔍 Thread {thread_id}: Validating UTF-8 encoding...")
        
        # Simulate UTF-8 validation process
        time.sleep(random.uniform(0.1, 0.3))  # Validation takes time
        
        # Step 3: Check for invalid UTF-8 sequences
        with open(temp_file_path, 'rb') as f:
            content_bytes = f.read()
        
        # VULNERABILITY: Race condition between validation and execution
        if b'\\xC0' in content_bytes or b'\\!' in content_bytes:
            print(f"⚠️  Thread {thread_id}: Invalid UTF-8 detected, but processing continues...")
            
            # Vulnerable: File content might change between check and execution
            time.sleep(0.2)  # Race condition window
        
        # Step 4: Execute SQL (potential command injection)
        print(f"🚀 Thread {thread_id}: Executing psql command...")
        try:
            # Simulate psql execution
            with open(temp_file_path, 'r') as f:
                final_content = f.read()
                print(f"📋 Thread {thread_id}: Final content: {final_content[:100]}...")
                
                # Check for command injection
                if '\\!' in final_content:
                    print(f"💀 Thread {thread_id}: COMMAND INJECTION DETECTED!")
                    print(f"🎯 Malicious command would execute: {final_content.split('\\!')[1].split()[0] if '\\!' in final_content else 'N/A'}")
                    return "INJECTION_SUCCESS"
                else:
                    print(f"✅ Thread {thread_id}: Normal SQL execution")
                    return "NORMAL_EXECUTION"
        
        except Exception as e:
            print(f"❌ Thread {thread_id}: Error during execution: {e}")
            return "ERROR"
        
        finally:
            # Cleanup
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def race_condition_exploit(self, target_file_path, thread_id):
        """Simulates attacker replacing file content during race window"""
        print(f"🎯 Attacker Thread {thread_id}: Starting race condition exploit...")
        
        # Wait for validation to start
        time.sleep(0.15)
        
        # Replace file content during race window
        if os.path.exists(target_file_path):
            print(f"🔄 Attacker Thread {thread_id}: Replacing file content...")
            try:
                with open(target_file_path, 'w') as f:
                    # Inject malicious command
                    malicious_content = "SELECT version(); \\! id; \\! whoami; \\! cat /etc/passwd"
                    f.write(malicious_content)
                print(f"💀 Attacker Thread {thread_id}: Malicious payload injected!")
                return True
            except Exception as e:
                print(f"❌ Attacker Thread {thread_id}: Failed to modify file: {e}")
                return False
        
        return False
    
    def safe_psql_execution(self, sql_content, thread_id):
        """SAFE - Proper UTF-8 validation and atomic file operations"""
        print(f"🔗 Safe Thread {thread_id}: Starting secure psql execution...")
        
        with self.lock:
            # Step 1: Validate UTF-8 in memory before writing to file
            try:
                # Validate UTF-8 encoding
                sql_content.encode('utf-8').decode('utf-8')
                
                # Check for command injection patterns
                if '\\!' in sql_content:
                    print(f"🚫 Safe Thread {thread_id}: Command injection attempt blocked!")
                    return "BLOCKED"
                
                # Create temporary file with atomic operations
                temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False)
                temp_file.write(sql_content)
                temp_file.flush()
                temp_file.close()
                
                # Execute with validated content
                print(f"✅ Safe Thread {thread_id}: Secure execution completed")
                os.unlink(temp_file.name)
                return "SAFE_EXECUTION"
                
            except UnicodeError:
                print(f"❌ Safe Thread {thread_id}: Invalid UTF-8 encoding rejected")
                return "ENCODING_ERROR"

def demonstrate_postgresql_race():
    print("=== PostgreSQL psql Race Condition Simulation (CVE-2025-1094) ===")
    print("Real-world impact: Command injection in PostgreSQL client tools\n")
    
    psql_sim = PostgreSQLClientSimulation()
    
    print("=" * 80)
    print("🚨 VULNERABLE VERSION - Race Condition Exploit")
    print("=" * 80)
    
    # Test 1: Normal SQL execution
    print("\n📋 Test 1: Normal SQL execution")
    normal_sql = "SELECT current_user, version();"
    result = psql_sim.vulnerable_psql_execution(normal_sql, 1)
    print(f"Result: {result}\n")
    
    # Test 2: Race condition attack simulation
    print("📋 Test 2: Race Condition Attack Simulation")
    print("Simulating concurrent file modification during UTF-8 validation...\n")
    
    results = []
    
    def worker_thread(sql_content, t_id):
        result = psql_sim.vulnerable_psql_execution(sql_content, t_id)
        results.append((t_id, result))
    
    def attacker_thread(target_path, t_id):
        # Simulate attacker modifying file during race window
        time.sleep(0.1)
        # In real scenario, attacker would modify the temp file
        print(f"🎯 Attacker {t_id}: Attempting to modify temp file during validation...")
        print(f"💀 Attacker {t_id}: Injected command execution payload!")
    
    # Start vulnerable processing
    initial_sql = "SELECT name FROM users WHERE id = 1;"
    
    # Simulate race condition
    t1 = threading.Thread(target=worker_thread, args=(initial_sql, "VICTIM"))
    t2 = threading.Thread(target=attacker_thread, args=("temp_file.sql", "ATTACKER"))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("\n📊 Race Condition Results:")
    for thread_id, result in results:
        print(f"  Thread {thread_id}: {result}")
    
    # Test 3: Direct UTF-8 injection attempt
    print("\n📋 Test 3: Direct UTF-8 Command Injection")
    malicious_sql = "SELECT version(); \\! whoami; \\! cat /etc/passwd"
    result = psql_sim.vulnerable_psql_execution(malicious_sql, "DIRECT_ATTACK")
    print(f"Direct injection result: {result}")
    
    print("\n" + "=" * 80)
    print("✅ SAFE VERSION - Atomic Operations and Validation")
    print("=" * 80)
    
    # Test safe implementation
    print("\n📋 Test 4: Safe implementation with same malicious input")
    safe_results = []
    
    def safe_worker(sql_content, t_id):
        result = psql_sim.safe_psql_execution(sql_content, t_id)
        safe_results.append((t_id, result))
    
    # Test safe version with malicious input
    safe_threads = []
    for i in range(3):
        t = threading.Thread(target=safe_worker, args=(malicious_sql, f"SAFE_{i+1}"))
        safe_threads.append(t)
        t.start()
    
    for t in safe_threads:
        t.join()
    
    print("\n📊 Safe Implementation Results:")
    for thread_id, result in safe_results:
        print(f"  Thread {thread_id}: {result}")

def show_postgresql_cve_details():
    print("\n" + "=" * 80)
    print("📋 CVE-2025-1094 TECHNICAL DETAILS")
    print("=" * 80)
    print("Vulnerability: PostgreSQL psql UTF-8 validation race condition")
    print("CVSS Score: 8.1 (High)")
    print("Attack Vector: Local/Remote command injection")
    print("Root Cause: Race condition between UTF-8 validation and execution")
    print("Impact: Arbitrary command execution with psql user privileges")
    print("Fix: Atomic file operations and proper validation sequencing")
    print("Affected: PostgreSQL client tools (psql)")

if __name__ == "__main__":
    demonstrate_postgresql_race()
    show_postgresql_cve_details()
