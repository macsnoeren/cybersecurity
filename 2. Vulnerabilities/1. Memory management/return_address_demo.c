// return_address_demo.c
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void secret_function() {
    printf("🎯 SUCCESS: You've hijacked the execution flow!\n");
    printf("🚨 This demonstrates how buffer overflows can redirect program execution\n");
    printf("💀 In a real attack, this could execute malicious shellcode\n");
}

void normal_function() {
    printf("✅ Normal execution path - this should be called\n");
}

void vulnerable_input(char* user_input) {
    char buffer[64];  // 64-byte buffer
    printf("Buffer address: %p\n", buffer);
    printf("Copying user input into buffer...\n");
    
    // VULNERABLE: No bounds checking
    strcpy(buffer, user_input);
    
    printf("Buffer contents: %.100s\n", buffer);
    printf("Returning from vulnerable_input...\n");
}

int main(int argc, char* argv[]) {
    printf("=== Return Address Manipulation Demo ===\n");
    printf("secret_function address: %p\n", secret_function);
    printf("normal_function address: %p\n", normal_function);
    printf("main function address: %p\n", main);
    
    if (argc != 2) {
        printf("\nUsage: %s <input_string>\n", argv[0]);
        printf("Try: %s \"Normal input\"\n", argv[0]);
        printf("Then try with a very long string to trigger overflow\n");
        return 1;
    }
    
    printf("\n--- Before calling vulnerable function ---\n");
    vulnerable_input(argv[1]);
    printf("--- After vulnerable function returned ---\n");
    
    normal_function();  // This should execute normally
    
    printf("Program completed normally\n");
    return 0;
}
