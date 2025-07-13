#!/usr/bin/env python3
"""
Test runner for the Cybersecurity Operations Orchestrator
Provides various testing scenarios without requiring real API calls or targets
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime

def simulate_full_pentest():
    """Simulate a complete penetration test workflow"""
    print("🔍 Simulating Complete Penetration Test")
    print("=" * 50)
    
    # Simulate the LLM decision-making process
    test_scenarios = [
        {
            "iteration": 1,
            "phase": "Initial Reconnaissance",
            "llm_analysis": "New target detected. No previous scan data available. Starting with fast port scan to identify open services.",
            "command": "nmap -F --open -oN nmap_fast_scan 127.0.0.1",
            "simulated_output": """Starting Nmap 7.80 ( https://nmap.org ) at 2025-07-11 15:12 EST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00010s latency).
Not shown: 4094 closed ports
PORT     STATE SERVICE
135/tcp  open  msrpc
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5040/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 2.14 seconds""",
            "state_update": {
                "target_ip": "127.0.0.1",
                "open_ports": [
                    {"port": 135, "service": "msrpc", "version": None},
                    {"port": 445, "service": "microsoft-ds", "version": None},
                    {"port": 3389, "service": "ms-wbt-server", "version": None},
                    {"port": 5040, "service": "unknown", "version": None}
                ],
                "vulnerabilities": [],
                "web_directories": [],
                "notes": "Initial fast scan completed. Found 4 open ports on Windows system."
            }
        },
        {
            "iteration": 2,
            "phase": "Service Enumeration",
            "llm_analysis": "Fast scan revealed Windows services. Need detailed service and version information for vulnerability assessment.",
            "command": "nmap -sV -sC -p 135,445,3389,5040 -oN nmap_service_scan 127.0.0.1",
            "simulated_output": """Starting Nmap 7.80 ( https://nmap.org ) at 2025-07-11 15:14 EST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00020s latency).

PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
445/tcp  open  microsoft-ds  Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5040/tcp open  unknown

Host script results:
|_clock-skew: mean: 0s, deviation: 0s, median: 0s
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-07-11T20:14:30
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.52 seconds""",
            "state_update": {
                "target_ip": "127.0.0.1",
                "open_ports": [
                    {"port": 135, "service": "msrpc", "version": "Microsoft Windows RPC"},
                    {"port": 445, "service": "microsoft-ds", "version": "Microsoft Windows 7-10"},
                    {"port": 3389, "service": "ms-wbt-server", "version": "Microsoft Terminal Services"},
                    {"port": 5040, "service": "unknown", "version": "Unknown"}
                ],
                "vulnerabilities": [],
                "web_directories": [],
                "notes": "Service enumeration complete. Windows system with SMB and RDP services exposed."
            }
        },
        {
            "iteration": 3,
            "phase": "Vulnerability Assessment",
            "llm_analysis": "Windows system with SMB exposed. Checking for common SMB vulnerabilities and enumeration opportunities.",
            "command": "nmap --script smb-vuln* -p 445 127.0.0.1",
            "simulated_output": """Starting Nmap 7.80 ( https://nmap.org ) at 2025-07-11 15:16 EST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00010s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to Remote Code Execution (MS08-067)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|       The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|       Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|       code via a crafted RPC request that triggers the overflow during path canonicalization.
|       
|     Disclosure date: 2008-10-23
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
|_      https://technet.microsoft.com/en-us/library/security/ms08-067.aspx

Nmap done: 1 IP address (1 host up) scanned in 5.21 seconds""",
            "state_update": {
                "target_ip": "127.0.0.1",
                "open_ports": [
                    {"port": 135, "service": "msrpc", "version": "Microsoft Windows RPC"},
                    {"port": 445, "service": "microsoft-ds", "version": "Microsoft Windows 7-10"},
                    {"port": 3389, "service": "ms-wbt-server", "version": "Microsoft Terminal Services"},
                    {"port": 5040, "service": "unknown", "version": "Unknown"}
                ],
                "vulnerabilities": [
                    {
                        "cve": "CVE-2008-4250",
                        "description": "Microsoft Windows system vulnerable to Remote Code Execution (MS08-067)",
                        "port": 445,
                        "severity": "critical"
                    }
                ],
                "web_directories": [],
                "notes": "Critical vulnerability found: MS08-067 RCE vulnerability in SMB service."
            }
        }
    ]
    
    # Create output directory
    output_dir = Path("test_pentest_results")
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Results will be saved to: {output_dir}")
    print()
    
    # Simulate the workflow
    for scenario in test_scenarios:
        print(f"🔄 Iteration {scenario['iteration']} - {scenario['phase']}")
        print(f"📊 LLM Analysis: {scenario['llm_analysis']}")
        print(f"⚡ Command: {scenario['command']}")
        print("🔍 Executing command...")
        
        # Simulate command execution time
        time.sleep(2)
        
        # Save command and output
        cmd_file = output_dir / f"command_{scenario['iteration']:03d}.txt"
        output_file = output_dir / f"output_{scenario['iteration']:03d}.txt"
        
        with open(cmd_file, 'w') as f:
            f.write(f"Command #{scenario['iteration']}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Phase: {scenario['phase']}\n")
            f.write(f"Command: {scenario['command']}\n")
        
        with open(output_file, 'w') as f:
            f.write(scenario['simulated_output'])
        
        print(f"✅ Command completed")
        print(f"📋 Found: {len(scenario['state_update'].get('open_ports', []))} ports, {len(scenario['state_update'].get('vulnerabilities', []))} vulnerabilities")
        print("-" * 50)
    
    # Generate final report
    final_state = test_scenarios[-1]['state_update']
    generate_test_report(final_state, output_dir)
    
    print("🎉 Simulation completed!")
    print(f"📄 Check {output_dir} for all results")

def generate_test_report(state, output_dir):
    """Generate a sample penetration test report"""
    report = f"""# Penetration Test Report

## Executive Summary

**Target:** {state['target_ip']}  
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tester:** COO (Cybersecurity Operations Orchestrator)  

### Key Findings
- **Open Ports:** {len(state['open_ports'])} discovered
- **Vulnerabilities:** {len(state['vulnerabilities'])} identified
- **Risk Level:** {"Critical" if any(v.get('severity') == 'critical' for v in state['vulnerabilities']) else "Medium"}

## Technical Findings

### Open Ports
"""
    
    for port_info in state['open_ports']:
        report += f"- **Port {port_info['port']}:** {port_info['service']} ({port_info['version']})\n"
    
    report += "\n### Vulnerabilities\n"
    
    for vuln in state['vulnerabilities']:
        report += f"""
#### {vuln['cve']} - {vuln['severity'].upper()}
- **Port:** {vuln['port']}
- **Description:** {vuln['description']}
"""
    
    report += """
## Recommendations

1. **Immediate Actions:**
   - Patch the MS08-067 vulnerability immediately
   - Disable SMB if not required
   - Enable Windows Firewall with restrictive rules

2. **Security Hardening:**
   - Implement network segmentation
   - Enable audit logging
   - Regular vulnerability scanning
   - Update management process

3. **Monitoring:**
   - Monitor for suspicious SMB activity
   - Implement intrusion detection
   - Regular security assessments

## Methodology

This test was conducted using the COO (Cybersecurity Operations Orchestrator) which combines:
- Automated tool execution (nmap, gobuster, nikto, etc.)
- AI-powered decision making via Groq LLM
- Structured vulnerability assessment

The test followed standard penetration testing methodology:
1. Reconnaissance
2. Enumeration
3. Vulnerability Assessment
4. Exploitation Planning
5. Reporting

---
*Report generated by COO - Cybersecurity Operations Orchestrator*
"""
    
    report_file = output_dir / "final_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"📊 Final report generated: {report_file}")

def test_api_connection():
    """Test the Groq API connection without running a full pentest"""
    print("🔌 Testing Groq API Connection")
    print("=" * 35)
    
    # Check if API key is configured
    from config import Config
    api_key = Config.get_groq_api_key()
    
    if not api_key:
        print("❌ No API key found!")
        print("Run: python setup_api_key.py")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test API call
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        test_payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": "Respond with just 'API test successful'"}
            ],
            "max_tokens": 10
        }
        
        print("🔄 Testing API connection...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            api_response = result['choices'][0]['message']['content']
            print(f"✅ API test successful!")
            print(f"📝 LLM response: {api_response}")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def show_expected_output():
    """Show what typical orchestrator output looks like"""
    print("📋 Expected Orchestrator Output")
    print("=" * 35)
    
    sample_output = """
🚀 TYPICAL ORCHESTRATOR SESSION OUTPUT:

2025-07-11 15:12:34,123 - INFO - Starting penetration test against 192.168.1.100
2025-07-11 15:12:34,125 - INFO - Results will be saved to: pentest_results

============================================================
ITERATION 1
============================================================
2025-07-11 15:12:34,126 - INFO - Sending request to Groq API...
2025-07-11 15:12:34,890 - INFO - Received response from Groq API: 1247 characters
2025-07-11 15:12:34,891 - INFO - LLM Analysis: Initial state. No data available. Performing fast TCP port scan to identify initial attack surface.
2025-07-11 15:12:34,892 - INFO - Executing command #1: nmap -F --open -oN nmap_fast_scan 192.168.1.100
2025-07-11 15:12:37,456 - INFO - Command completed with return code: 0

============================================================
ITERATION 2
============================================================
2025-07-11 15:12:38,457 - INFO - Sending request to Groq API...
2025-07-11 15:12:39,123 - INFO - Received response from Groq API: 1456 characters
2025-07-11 15:12:39,124 - INFO - LLM Analysis: Fast scan identified open ports 22 (SSH), 80 (HTTP), 443 (HTTPS). Now performing detailed service and version scan.
2025-07-11 15:12:39,125 - INFO - Executing command #2: nmap -sV -sC -p 22,80,443 -oN nmap_service_scan 192.168.1.100
2025-07-11 15:12:45,789 - INFO - Command completed with return code: 0

============================================================
ITERATION 3
============================================================
2025-07-11 15:12:46,790 - INFO - Sending request to Groq API...
2025-07-11 15:12:47,234 - INFO - Received response from Groq API: 1589 characters
2025-07-11 15:12:47,235 - INFO - LLM Analysis: Service scan confirms Apache httpd 2.4.41 on port 80. Enumerating web directories to find potential attack vectors.
2025-07-11 15:12:47,236 - INFO - Executing command #3: gobuster dir -u http://192.168.1.100 -w wordlists/common.txt -x php,html,txt
2025-07-11 15:12:52,123 - INFO - Command completed with return code: 0

[... continues for more iterations ...]

============================================================
FINAL ITERATION
============================================================
2025-07-11 15:15:23,456 - INFO - LLM indicated test completion
2025-07-11 15:15:23,457 - INFO - Final report saved to: pentest_results/final_report.md
2025-07-11 15:15:23,458 - INFO - Penetration test completed
2025-07-11 15:15:23,459 - INFO - Total commands executed: 8
2025-07-11 15:15:23,460 - INFO - Session duration: 0:02:49.337854

📁 GENERATED FILES:
pentest_results/
├── orchestrator_20250711_151234.log     # Complete execution log
├── session_state.json                   # Final state data
├── final_report.md                      # Markdown report
├── command_001.txt → command_008.txt    # Individual commands
└── output_001.txt → output_008.txt      # Tool outputs

📊 FINAL REPORT CONTENT:
- Executive summary with risk assessment
- Detailed port and service information
- Vulnerability findings with CVE references
- Web directories and interesting files discovered
- Specific recommendations for remediation
"""
    
    print(sample_output)

def main():
    """Main test menu"""
    print("🧪 COO Testing Suite")
    print("=" * 25)
    print("Choose a test option:")
    print("1. Full Penetration Test Simulation")
    print("2. Test Groq API Connection")
    print("3. Show Expected Output Examples")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print()
            simulate_full_pentest()
            break
        elif choice == "2":
            print()
            test_api_connection()
            break
        elif choice == "3":
            print()
            show_expected_output()
            break
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
