// buffer_overflow_demo.c
#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[10];  // Small buffer - vulnerability point
    printf("Before strcpy: buffer address = %p\n", buffer);
    strcpy(buffer, input);  // No bounds checking!
    printf("Buffer contains: %s\n", buffer);
    printf("Function completed successfully\n");
}

int main() {
    printf("=== Buffer Overflow Demonstration ===\n");
    printf("Buffer size is 10 bytes\n\n");
    
    // Safe input
    printf("Test 1: Safe input (9 characters)\n");
    vulnerable_function("SafeInput");
    
    printf("\nTest 2: Overflow input (20 characters)\n");
    vulnerable_function("ThisInputIsTooLongForBuffer");
    
    return 0;
}