import threading
import time
import random

class BankAccount:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.lock = threading.Lock()  # For safe version
    
    def withdraw_unsafe(self, amount, thread_id):
        """Unsafe withdrawal - race condition possible"""
        print(f"Thread {thread_id}: Checking balance...")
        if self.balance >= amount:
            print(f"Thread {thread_id}: Balance sufficient ({self.balance}), withdrawing {amount}")
            # Simulate network delay or processing time
            time.sleep(random.uniform(0.1, 0.3))
            self.balance -= amount
            print(f"Thread {thread_id}: Withdrawal complete. New balance: {self.balance}")
            return True
        else:
            print(f"Thread {thread_id}: Insufficient funds")
            return False
    
    def withdraw_safe(self, amount, thread_id):
        """Safe withdrawal with locking"""
        with self.lock:
            print(f"Thread {thread_id}: Acquired lock, checking balance...")
            if self.balance >= amount:
                print(f"Thread {thread_id}: Balance sufficient ({self.balance}), withdrawing {amount}")
                time.sleep(random.uniform(0.1, 0.3))
                self.balance -= amount
                print(f"Thread {thread_id}: Withdrawal complete. New balance: {self.balance}")
                return True
            else:
                print(f"Thread {thread_id}: Insufficient funds")
                return False

def demonstrate_race_condition():
    print("=== Race Condition Demonstration ===\n")
    
    # Unsafe version
    print("UNSAFE VERSION (Race Condition Possible):")
    account1 = BankAccount(1000)
    
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=account1.withdraw_unsafe, 
            args=(800, i+1)
        )
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Final balance (unsafe): {account1.balance}")
    print("\n" + "="*50 + "\n")
    
    # Safe version
    print("SAFE VERSION (With Locking):")
    account2 = BankAccount(1000)
    
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=account2.withdraw_safe, 
            args=(800, i+1)
        )
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Final balance (safe): {account2.balance}")

if __name__ == "__main__":
    demonstrate_race_condition()