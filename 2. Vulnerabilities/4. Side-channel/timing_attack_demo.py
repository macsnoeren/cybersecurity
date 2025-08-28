# timing_attack_demo.py
import time
import hashlib
import statistics
import random

class AuthenticationSystem:
    def __init__(self):
        # Simulate stored password hash
        self.stored_password_hash = hashlib.sha256("secretpassword123".encode()).hexdigest()
        self.stored_username = "admin"
    
    def vulnerable_authenticate(self, username, password):
        """VULNERABLE - Early termination reveals information via timing"""
        # Check username first - early return on mismatch
        if username != self.stored_username:
            return False
        
        # Hash the provided password
        provided_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Character-by-character comparison (vulnerable to timing attack)
        for i in range(len(self.stored_password_hash)):
            if i >= len(provided_hash) or provided_hash[i] != self.stored_password_hash[i]:
                return False
            # Simulate some processing time per character
            time.sleep(0.0001)  # 0.1ms per character
        
        return True
    
    def safe_authenticate(self, username, password):
        """SAFE - Constant time comparison"""
        # Hash the provided password
        provided_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Always check both username and password hash
        username_match = (username == self.stored_username)
        
        # Constant-time comparison
        hash_match = self.constant_time_compare(provided_hash, self.stored_password_hash)
        
        # Add constant delay to mask timing differences
        time.sleep(0.01)  # 10ms constant delay
        
        return username_match and hash_match
    
    def constant_time_compare(self, a, b):
        """Constant time string comparison"""
        if len(a) != len(b):
            # Still compare to maintain constant time
            b = "0" * len(a)
        
        result = 0
        for i in range(len(a)):
            result |= ord(a[i]) ^ ord(b[i])
        
        return result == 0

def measure_timing(auth_system, username, password, iterations=10):
    """Measure average authentication time"""
    times = []
    for _ in range(iterations):
        start_time = time.time()
        auth_system.vulnerable_authenticate(username, password)
        end_time = time.time()
        times.append((end_time - start_time) * 1000)  # Convert to milliseconds
    
    return statistics.mean(times)

def demonstrate_timing_attack():
    print("=== Timing Attack Demonstration ===\n")
    
    auth = AuthenticationSystem()
    print(f"Target username: {auth.stored_username}")
    print(f"Target password hash: {auth.stored_password_hash[:16]}...\n")
    
    # Test different scenarios
    test_cases = [
        ("wronguser", "wrongpass", "Wrong username"),
        ("admin", "wrongpass", "Correct username, wrong password"),
        ("admin", "secretpassword123", "Correct credentials"),
        ("admin", "secretpassword000", "Almost correct password"),
    ]
    
    print("VULNERABLE VERSION - Timing Measurements:")
    print("-" * 60)
    
    for username, password, description in test_cases:
        avg_time = measure_timing(auth, username, password)
        print(f"{description:30} | Avg time: {avg_time:.2f}ms")
    
    print("\n" + "="*60 + "\n")
    
    # Demonstrate how attacker could exploit timing differences
    print("Simulated Attack: Finding correct username")
    usernames_to_test = ["user", "guest", "admin", "root", "test"]
    
    username_times = {}
    for username in usernames_to_test:
        avg_time = measure_timing(auth, username, "dummy_password")
        username_times[username] = avg_time
        print(f"Username '{username:10}' | Avg time: {avg_time:.2f}ms")
    
    # Find username with longest time (indicating it passed username check)
    suspected_username = max(username_times.items(), key=lambda x: x[1])
    print(f"\nSuspected correct username: '{suspected_username[0]}' (longest time: {suspected_username[1]:.2f}ms)")
    
    print("\n" + "="*60 + "\n")
    
    # Test safe version
    print("SAFE VERSION - Constant Time:")
    print("-" * 40)
    
    safe_times = []
    for username, password, description in test_cases:
        times = []
        for _ in range(5):
            start_time = time.time()
            auth.safe_authenticate(username, password)
            end_time = time.time()
            times.append((end_time - start_time) * 1000)
        
        avg_time = statistics.mean(times)
        safe_times.append(avg_time)
        print(f"{description:30} | Avg time: {avg_time:.2f}ms")
    
    print(f"\nTiming variation (safe): {max(safe_times) - min(safe_times):.2f}ms")

if __name__ == "__main__":
    demonstrate_timing_attack()