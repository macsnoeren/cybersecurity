// sophos_xg_buffer_demo.c - Educational simulation of CVE-2020-15069
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_USER_AGENT 256
#define MAX_REQUEST_SIZE 1024

// Simulates vulnerable HTTP request parsing in firewall
void process_http_request(char* user_agent, char* request_data) {
    char buffer[MAX_USER_AGENT];  // 256-byte buffer
    char log_entry[512];
    
    printf("🔥 Firewall: Processing HTTP request...\n");
    printf("📡 User-Agent: %s\n", user_agent);
    
    // VULNERABLE: No length validation on User-Agent header
    strcpy(buffer, user_agent);  // Buffer overflow potential
    
    // Additional processing
    snprintf(log_entry, sizeof(log_entry), 
             "HTTP Request from User-Agent: %s", buffer);
    
    printf("📝 Log entry: %.100s\n", log_entry);
    printf("✅ Request processed\n");
}

void firewall_admin_function() {
    printf("🎯 CRITICAL: Firewall admin function executed!\n");
    printf("💀 Attacker could now:\n");
    printf("   - Disable firewall rules\n");
    printf("   - Access internal network\n");
    printf("   - Install backdoors\n");
    printf("   - Exfiltrate network traffic\n");
}

int main(int argc, char* argv[]) {
    printf("=== Sophos XG Firewall Buffer Overflow Simulation (CVE-2020-15069) ===\n");
    printf("Real-world impact: RCE on firewall devices, network compromise\n\n");
    
    if (argc != 2) {
        printf("Usage: %s \"<user_agent_string>\"\n", argv[0]);
        printf("Normal:  %s \"Mozilla/5.0 (Windows NT 10.0; Win64; x64)\"\n", argv[0]);
        printf("Attack:  %s \"$(python3 -c 'print(\"A\"*300)')\"\n", argv[0]);
        return 1;
    }
    
    printf("Firewall admin function located at: %p\n", firewall_admin_function);
    printf("Buffer overflow target: process_http_request()\n\n");
    
    process_http_request(argv[1], "GET / HTTP/1.1");
    
    printf("\n--- Normal firewall operation should continue ---\n");
    return 0;
}