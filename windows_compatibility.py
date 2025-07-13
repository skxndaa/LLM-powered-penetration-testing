#!/usr/bin/env python3
"""
Windows-compatible tool fallbacks for the Cybersecurity Operations Orchestrator
"""

import os
import subprocess
from pathlib import Path

def check_tool_availability():
    """Check which tools are available and suggest Windows alternatives"""
    tools = {
        'nmap': 'Network scanning',
        'gobuster': 'Directory enumeration', 
        'nikto': 'Web vulnerability scanning',
        'curl': 'HTTP requests',
        'powershell': 'Windows PowerShell'
    }
    
    available = {}
    alternatives = {}
    
    print("🔍 Checking tool availability...")
    print("-" * 40)
    
    for tool, description in tools.items():
        try:
            if tool == 'powershell':
                result = subprocess.run(['powershell', '-Command', 'Get-Host'], 
                                      capture_output=True, timeout=5)
            else:
                result = subprocess.run([tool, '--version'], 
                                      capture_output=True, timeout=5)
            
            if result.returncode == 0:
                available[tool] = True
                print(f"✅ {tool}: Available")
            else:
                available[tool] = False
                print(f"❌ {tool}: Not available")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            available[tool] = False
            print(f"❌ {tool}: Not available")
    
    # Suggest Windows alternatives
    if not available.get('nmap', False):
        alternatives['nmap'] = {
            'windows_native': ['netstat', 'telnet', 'Test-NetConnection'],
            'download_link': 'https://nmap.org/download.html',
            'chocolatey': 'choco install nmap'
        }
    
    if not available.get('curl', False) and available.get('powershell', False):
        alternatives['curl'] = {
            'windows_native': ['Invoke-WebRequest', 'Invoke-RestMethod'],
            'note': 'PowerShell has built-in web request capabilities'
        }
    
    return available, alternatives

def generate_windows_compatible_commands():
    """Generate Windows-compatible scanning commands"""
    commands = {
        'port_scan_localhost': [
            'netstat -an | findstr LISTENING',
            'powershell "Get-NetTCPConnection | Where-Object {$_.State -eq \'Listen\'}"'
        ],
        'network_connectivity': [
            'ping -n 4 127.0.0.1',
            'powershell "Test-NetConnection -ComputerName 127.0.0.1 -Port 80"'
        ],
        'service_check': [
            'powershell "Get-Service | Where-Object {$_.Status -eq \'Running\'}"',
            'sc query type=service state=all'
        ],
        'web_request': [
            'powershell "Invoke-WebRequest -Uri http://127.0.0.1 -UseBasicParsing"',
            'curl http://127.0.0.1'
        ]
    }
    
    return commands

def install_tools_windows():
    """Provide instructions for installing tools on Windows"""
    print("\n🛠️ Installing Penetration Testing Tools on Windows")
    print("=" * 55)
    
    print("\n📋 Option 1: Using Chocolatey (Recommended)")
    print("-" * 45)
    print("1. Install Chocolatey if not already installed:")
    print("   PowerShell (Run as Administrator):")
    print("   Set-ExecutionPolicy Bypass -Scope Process -Force;")
    print("   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;")
    print("   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")
    print()
    print("2. Install tools:")
    print("   choco install nmap")
    print("   choco install curl")
    print()
    
    print("📋 Option 2: Manual Installation")
    print("-" * 35)
    print("1. nmap: Download from https://nmap.org/download.html")
    print("   - Choose 'Latest stable release self-installer'")
    print("   - Run installer and ensure 'Add to PATH' is checked")
    print()
    print("2. curl: Usually included with Windows 10+ or download from https://curl.se/windows/")
    print()
    
    print("📋 Option 3: Use Windows Subsystem for Linux (WSL)")
    print("-" * 55)
    print("1. Install WSL2: wsl --install")
    print("2. Install Ubuntu: wsl --install -d Ubuntu")  
    print("3. In WSL: sudo apt update && sudo apt install nmap gobuster dirb nikto")
    print()
    
    print("📋 Option 4: Use Windows Native Tools (Limited)")
    print("-" * 50)
    commands = generate_windows_compatible_commands()
    
    print("Port scanning with netstat:")
    for cmd in commands['port_scan_localhost']:
        print(f"   {cmd}")
    print()
    
    print("Network connectivity testing:")
    for cmd in commands['network_connectivity']:
        print(f"   {cmd}")

def create_windows_orchestrator():
    """Create a Windows-native version of basic orchestration"""
    print("\n🔧 Creating Windows-Compatible Test")
    print("=" * 40)
    
    # Test localhost port scanning
    print("🔍 Scanning localhost ports...")
    try:
        result = subprocess.run([
            'netstat', '-an'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Port scan successful!")
            
            # Parse listening ports
            listening_ports = []
            for line in result.stdout.split('\n'):
                if 'LISTENING' in line and '127.0.0.1' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        addr_port = parts[1]
                        if ':' in addr_port:
                            port = addr_port.split(':')[-1]
                            listening_ports.append(port)
            
            print(f"📊 Found {len(set(listening_ports))} listening ports on localhost:")
            for port in sorted(set(listening_ports)):
                print(f"   Port {port}")
        else:
            print("❌ Port scan failed")
            
    except Exception as e:
        print(f"❌ Error during port scan: {e}")
    
    # Test web connectivity
    print("\n🌐 Testing web connectivity...")
    try:
        result = subprocess.run([
            'powershell', '-Command',
            'try { Invoke-WebRequest -Uri "http://127.0.0.1" -UseBasicParsing -TimeoutSec 5 } catch { Write-Output "Connection failed: $_" }'
        ], capture_output=True, text=True, timeout=30)
        
        if 'StatusCode' in result.stdout:
            print("✅ Web server detected on localhost!")
            print("📄 Response preview:")
            print(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
        else:
            print("📝 No web server detected on port 80")
            print(f"Response: {result.stdout}")
            
    except Exception as e:
        print(f"❌ Error during web test: {e}")

def main():
    """Main function for Windows compatibility testing"""
    print("🪟 Windows Compatibility Checker for COO")
    print("=" * 45)
    
    # Check tool availability
    available, alternatives = check_tool_availability()
    
    # Show alternatives if tools are missing
    if alternatives:
        print(f"\n💡 Suggested Alternatives:")
        print("-" * 25)
        for tool, alts in alternatives.items():
            print(f"\n{tool}:")
            if 'windows_native' in alts:
                print(f"  Windows native: {', '.join(alts['windows_native'])}")
            if 'download_link' in alts:
                print(f"  Download: {alts['download_link']}")
            if 'chocolatey' in alts:
                print(f"  Chocolatey: {alts['chocolatey']}")
    
    # Offer to install tools
    print(f"\n🎯 What would you like to do?")
    print("1. Show tool installation instructions")
    print("2. Run Windows-native compatibility test")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        install_tools_windows()
    elif choice == "2":
        create_windows_orchestrator()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
