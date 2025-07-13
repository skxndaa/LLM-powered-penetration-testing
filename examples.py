#!/usr/bin/env python3
"""
Example usage and testing utilities for the Cybersecurity Operations Orchestrator
"""

import os
import json
import sys
from pathlib import Path
import subprocess
from datetime import datetime

def create_test_environment():
    """Create a test environment with sample data and configurations"""
    print("Creating test environment...")
    
    # Create directories
    test_dir = Path("test_environment")
    test_dir.mkdir(exist_ok=True)
    
    wordlists_dir = test_dir / "wordlists"
    wordlists_dir.mkdir(exist_ok=True)
    
    # Create sample wordlists
    sample_dirs = [
        "admin", "administrator", "login", "test", "backup", "config",
        "uploads", "images", "js", "css", "api", "v1", "v2", "old",
        "tmp", "temp", "logs", "data", "files", "docs", "downloads"
    ]
    
    with open(wordlists_dir / "directories.txt", "w") as f:
        f.write("\n".join(sample_dirs))
    
    print(f"✓ Test environment created at: {test_dir}")
    return test_dir

def simulate_nmap_output():
    """Generate sample nmap output for testing"""
    return """Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-15 10:30 EST
Nmap scan report for 192.168.1.100
Host is up (0.001s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https

Nmap done: 1 IP address (1 host up) scanned in 2.45 seconds"""

def simulate_service_scan():
    """Generate sample nmap service scan output"""
    return """Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-15 10:32 EST
Nmap scan report for 192.168.1.100
Host is up (0.001s latency).

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
80/tcp  open  http     Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page
443/tcp open  ssl/http Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2023-01-01T00:00:00
|_Not valid after:  2024-01-01T00:00:00
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.32 seconds"""

def simulate_gobuster_output():
    """Generate sample gobuster output"""
    return """=====================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
=====================================================
[+] Url:                     http://192.168.1.100
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Extensions:              php,txt,html
[+] Timeout:                 10s
=====================================================
2024/01/15 10:35:00 Starting gobuster in directory enumeration mode
=====================================================
/.htaccess            (Status: 403) [Size: 278]
/.htaccess.php        (Status: 403) [Size: 278]
/.htaccess.txt        (Status: 403) [Size: 278]
/.htaccess.html       (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/.hta.php             (Status: 403) [Size: 278]
/.hta.txt             (Status: 403) [Size: 278]
/.hta.html            (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htpasswd.php        (Status: 403) [Size: 278]
/.htpasswd.txt        (Status: 403) [Size: 278]
/.htpasswd.html       (Status: 403) [Size: 278]
/admin                (Status: 301) [Size: 312] [--> http://192.168.1.100/admin/]
/admin.php            (Status: 200) [Size: 1234]
/backup               (Status: 301) [Size: 313] [--> http://192.168.1.100/backup/]
/config.php           (Status: 200) [Size: 0]
/index.html           (Status: 200) [Size: 10918]
/login.php            (Status: 200) [Size: 1567]
/server-status        (Status: 403) [Size: 278]
/uploads              (Status: 301) [Size: 314] [--> http://192.168.1.100/uploads/]
=====================================================
2024/01/15 10:35:30 Finished
====================================================="""

def test_llm_json_parsing():
    """Test LLM JSON response parsing"""
    sample_response = {
        "analysis": "Fast scan identified open ports 22 (SSH), 80 (HTTP), and 443 (HTTPS). Need to perform service enumeration to identify versions and potential vulnerabilities.",
        "next_command": "nmap -sV -sC -p 22,80,443 -oN nmap_service_scan 192.168.1.100",
        "updated_state": {
            "target_ip": "192.168.1.100",
            "open_ports": [
                {"port": 22, "service": "ssh", "version": None},
                {"port": 80, "service": "http", "version": None},
                {"port": 443, "service": "https", "version": None}
            ],
            "vulnerabilities": [],
            "web_directories": [],
            "notes": "Initial port scan completed. Found 3 open ports."
        },
        "final_report": None
    }
    
    # Test JSON serialization
    try:
        json_str = json.dumps(sample_response, indent=2)
        parsed = json.loads(json_str)
        print("✓ JSON parsing test passed")
        return True
    except Exception as e:
        print(f"✗ JSON parsing test failed: {e}")
        return False

def run_dry_run():
    """Run a simulated penetration test without actual tool execution"""
    print("Running dry-run simulation...")
    print("=" * 50)
    
    # Simulate workflow
    steps = [
        {
            "step": 1,
            "command": "nmap -F --open 192.168.1.100",
            "output": simulate_nmap_output(),
            "analysis": "Initial port scan reveals 3 open ports: SSH (22), HTTP (80), HTTPS (443)"
        },
        {
            "step": 2,
            "command": "nmap -sV -sC -p 22,80,443 192.168.1.100",
            "output": simulate_service_scan(),
            "analysis": "Service enumeration shows Apache 2.4.41 on ports 80/443, OpenSSH 8.2p1 on port 22"
        },
        {
            "step": 3,
            "command": "gobuster dir -u http://192.168.1.100 -w /usr/share/wordlists/dirb/common.txt",
            "output": simulate_gobuster_output(),
            "analysis": "Web directory enumeration found admin panel, login page, and upload directory"
        }
    ]
    
    for step in steps:
        print(f"\nStep {step['step']}: {step['command']}")
        print(f"Analysis: {step['analysis']}")
        print(f"Output preview: {step['output'][:100]}...")
    
    print("\n✓ Dry-run completed successfully")

def check_dependencies():
    """Check if all required dependencies are available"""
    print("Checking dependencies...")
    
    # Check Python modules
    required_modules = ['requests', 'json', 'subprocess', 'pathlib']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"✗ Missing Python modules: {', '.join(missing_modules)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("✓ All Python dependencies available")
    
    # Check if curl/requests can reach Groq API
    try:
        import requests
        response = requests.get("https://api.groq.com", timeout=5)
        print("✓ Groq API endpoint reachable")
    except Exception as e:
        print(f"⚠ Groq API check failed: {e}")
    
    return True

def generate_sample_config():
    """Generate a sample configuration file"""
    config = {
        "groq_api_key": "YOUR_GROQ_API_KEY_HERE",
        "default_target": "192.168.1.100",
        "output_directory": "pentest_results",
        "max_iterations": 50,
        "tools": {
            "nmap": {
                "enabled": True,
                "path": "nmap",
                "timeout": 300
            },
            "gobuster": {
                "enabled": True,
                "path": "gobuster",
                "wordlist": "wordlists/directories.txt",
                "timeout": 600
            }
        },
        "notification": {
            "enabled": False,
            "webhook_url": "",
            "on_completion": True,
            "on_error": True
        }
    }
    
    config_file = Path("sample_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Sample configuration saved to: {config_file}")

def main():
    """Main function for example usage"""
    print("Cybersecurity Operations Orchestrator - Examples & Testing")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "test-env":
            create_test_environment()
        elif action == "dry-run":
            run_dry_run()
        elif action == "check-deps":
            check_dependencies()
        elif action == "sample-config":
            generate_sample_config()
        elif action == "test-json":
            test_llm_json_parsing()
        else:
            print(f"Unknown action: {action}")
    else:
        print("\nAvailable actions:")
        print("  python examples.py test-env      - Create test environment")
        print("  python examples.py dry-run      - Run simulation")
        print("  python examples.py check-deps   - Check dependencies")
        print("  python examples.py sample-config - Generate sample config")
        print("  python examples.py test-json    - Test JSON parsing")
        print("\nExample full usage:")
        print("  python orchestrator.py --target 192.168.1.100 --groq-api-key YOUR_KEY")

if __name__ == "__main__":
    main()
