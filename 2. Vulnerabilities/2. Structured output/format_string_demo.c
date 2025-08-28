// format_string_demo.c
#include <stdio.h>
#include <string.h>

int secret_value = 0x12345678;

void vulnerable_printf(char *user_input) {
    printf("User input: ");
    printf(user_input);  // VULNERABLE - user controls format string
    printf("\n");
}

void safe_printf(char *user_input) {
    printf("User input: %s\n", user_input);  // SAFE - format string is controlled
}

int main() {
    printf("=== Format String Vulnerability Demo ===\n");
    printf("Secret value stored at: %p (value: 0x%x)\n", &secret_value, secret_value);
    printf("\nTest 1: Normal string\n");
    vulnerable_printf("Hello World");
    
    printf("\nTest 2: Format string attack - reading stack\n");
    vulnerable_printf("%x %x %x %x");
    
    printf("\nTest 3: Format string attack - reading specific address\n");
    vulnerable_printf("%s");
    
    printf("\nTest 4: Safe version\n");
    safe_printf("%x %x %x %x");
    
    return 0;
}
