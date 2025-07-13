#!/usr/bin/env python3
"""
Configuration and utility functions for the Cybersecurity Operations Orchestrator
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class Config:
    """Configuration management for the orchestrator"""
    
    # Default tool configurations
    TOOLS = {
        "nmap": {
            "binary": "nmap",
            "fast_scan_flags": "-F --open",
            "service_scan_flags": "-sV -sC",
            "timeout": 300
        },
        "gobuster": {
            "binary": "gobuster",
            "default_wordlist": "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "extensions": "php,txt,html,asp,aspx,jsp",
            "timeout": 600
        },
        "nikto": {
            "binary": "nikto",
            "default_flags": "-h",
            "timeout": 300
        },
        "whatweb": {
            "binary": "whatweb",
            "default_flags": "-v",
            "timeout": 120
        },
        "sqlmap": {
            "binary": "sqlmap",
            "default_flags": "--batch --smart",
            "timeout": 600
        },
        "searchsploit": {
            "binary": "searchsploit",
            "default_flags": "",
            "timeout": 60
        },
        "dirb": {
            "binary": "dirb",
            "default_wordlist": "/usr/share/dirb/wordlists/common.txt",
            "timeout": 300
        }
    }
    
    # Groq API configuration
    GROQ_MODEL = "llama-3.1-8b-instant"  # Updated model
    GROQ_MAX_TOKENS = 1000
    GROQ_TEMPERATURE = 0.1
    GROQ_TIMEOUT = 30
    
    # Common wordlists for different platforms
    WORDLISTS = {
        "linux": {
            "directories": [
                "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
                "/usr/share/dirb/wordlists/common.txt",
                "/usr/share/wordlists/dirb/common.txt"
            ]
        },
        "windows": {
            "directories": [
                "wordlists/directory-list-2.3-medium.txt",
                "wordlists/common.txt"
            ]
        }
    }
    
    @staticmethod
    def get_wordlist(list_type: str = "directories") -> str:
        """Get the first available wordlist for the current platform"""
        platform = "windows" if os.name == 'nt' else "linux"
        wordlists = Config.WORDLISTS.get(platform, {}).get(list_type, [])
        
        for wordlist in wordlists:
            if os.path.exists(wordlist):
                return wordlist
        
        # Fallback to a generic filename
        return f"wordlists/{list_type}.txt"
    
    @staticmethod
    def validate_tools() -> Dict[str, bool]:
        """Check which tools are available on the system"""
        import subprocess
        
        tool_status = {}
        for tool_name, config in Config.TOOLS.items():
            try:
                subprocess.run(
                    [config["binary"], "--help"], 
                    capture_output=True, 
                    timeout=10
                )
                tool_status[tool_name] = True
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                tool_status[tool_name] = False
        
        return tool_status
    
    @staticmethod
    def get_groq_api_key() -> str:
        """Get Groq API key from various sources"""
        # Try environment variable first
        api_key = os.environ.get('GROQ_API_KEY')
        if api_key:
            return api_key
        
        # Try config file
        config_file = Path('groq_config.json')
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                    return config_data.get('api_key', '')
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return ""
    
    @staticmethod
    def save_groq_api_key(api_key: str):
        """Save Groq API key to config file"""
        config_file = Path('groq_config.json')
        config_data = {'api_key': api_key}
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"✓ API key saved to {config_file}")
        print("⚠️  Keep this file secure and don't share it!")

class PromptTemplates:
    """Template management for different types of LLM prompts"""
    
    SYSTEM_PROMPT = '''You are "COO" (Cybersecurity Operations Orchestrator), an expert-level penetration tester and AI assistant, running on the high-speed Groq platform. Your primary function is to direct a network penetration test by processing data, generating tool commands, and analyzing outputs in a structured, step-by-step manner.

**Your Core Directives:**

1. **Stateless Operation:** You operate one step at a time. You will be given the current "state" of the pentest and the output of the last tool you ran. Analyze this information and decide on the single best next action.

2. **Structured I/O:** You MUST communicate exclusively in JSON format. Do not provide any conversational text outside of the specified JSON structure.

3. **Command Generation:** Generate precise, single-line commands for cybersecurity tools. You do not execute these commands yourself.

4. **Tool Knowledge:** You are an expert in: `nmap`, `gobuster`, `dirb`, `nikto`, `whatweb`, `sqlmap`, `searchsploit`, and `msfconsole`.

5. **Analysis and Synthesis:** Analyze tool outputs to identify open ports, services, versions, potential vulnerabilities, interesting directories, and attack vectors.

6. **Pentesting Methodology:** Follow standard methodology:
   a. **Initial Reconnaissance:** Start with broad, non-intrusive scans
   b. **Enumeration:** Dig deeper into discovered services
   c. **Vulnerability Identification:** Correlate findings with known vulnerabilities
   d. **Exploitation Suggestion:** Suggest specific exploits or methods
   e. **Reporting:** Summarize findings into a coherent report

**JSON I/O Specification:**

**Input JSON:**
{
  "state": {
    "target_ip": "...",
    "open_ports": [{"port": 22, "service": "ssh", "version": "..."}],
    "vulnerabilities": [{"cve": "...", "description": "...", "port": 80}],
    "web_directories": ["/admin", "/login"],
    "notes": "..."
  },
  "last_tool_output": "Raw text output from the last executed command"
}

**Output JSON:**
{
  "analysis": "Brief expert analysis of the last_tool_output and its implications",
  "next_command": "Complete command to execute next (e.g., 'nmap -sV -p 80,443 192.168.1.10')",
  "updated_state": {
    // Full updated state object reflecting new analysis
  },
  "final_report": null // Or Markdown report string if next_command is "COMPLETE"
}

You must respond ONLY with valid JSON. No additional text or formatting outside the JSON structure.'''

    INITIAL_PROMPT = '''This is the beginning of a new penetration test. You have been given a target IP address. Your task is to start the reconnaissance phase with an appropriate initial scan. The state contains only the target IP and no previous scan data.'''

    COMPLETION_PROMPT = '''The user has requested to complete the penetration test. Please analyze all the gathered information and provide a comprehensive final report in Markdown format. Set next_command to "COMPLETE" and include the full report in final_report.'''

class StateManager:
    """Manages penetration test state persistence and validation"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.state_file = output_dir / "persistent_state.json"
    
    def save_state(self, state: Dict[str, Any], metadata: Dict[str, Any] = None):
        """Save current state to disk"""
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "metadata": metadata or {}
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
    
    def load_state(self) -> Dict[str, Any]:
        """Load state from disk if it exists"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                return data.get("state", {})
        return {}
    
    def validate_state(self, state: Dict[str, Any]) -> bool:
        """Validate state structure"""
        required_keys = ["target_ip", "open_ports", "vulnerabilities", "web_directories", "notes"]
        return all(key in state for key in required_keys)

class ReportGenerator:
    """Generates various types of reports from penetration test data"""
    
    @staticmethod
    def generate_executive_summary(state: Dict[str, Any]) -> str:
        """Generate executive summary from state"""
        target_ip = state.get("target_ip", "Unknown")
        open_ports = state.get("open_ports", [])
        vulnerabilities = state.get("vulnerabilities", [])
        
        summary = f"""# Executive Summary

## Target Information
- **Target IP:** {target_ip}
- **Scan Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Findings
- **Open Ports:** {len(open_ports)} discovered
- **Vulnerabilities:** {len(vulnerabilities)} identified
- **Risk Level:** {"High" if vulnerabilities else "Medium" if open_ports else "Low"}

"""
        return summary
    
    @staticmethod
    def generate_technical_details(state: Dict[str, Any]) -> str:
        """Generate detailed technical findings"""
        details = "## Technical Findings\n\n"
        
        # Open ports section
        open_ports = state.get("open_ports", [])
        if open_ports:
            details += "### Open Ports\n\n"
            for port_info in open_ports:
                port = port_info.get("port", "Unknown")
                service = port_info.get("service", "Unknown")
                version = port_info.get("version", "Unknown")
                details += f"- **Port {port}:** {service} ({version})\n"
            details += "\n"
        
        # Vulnerabilities section
        vulnerabilities = state.get("vulnerabilities", [])
        if vulnerabilities:
            details += "### Vulnerabilities\n\n"
            for vuln in vulnerabilities:
                cve = vuln.get("cve", "Unknown")
                description = vuln.get("description", "No description")
                port = vuln.get("port", "Unknown")
                details += f"- **{cve}** (Port {port}): {description}\n"
            details += "\n"
        
        # Web directories section
        web_dirs = state.get("web_directories", [])
        if web_dirs:
            details += "### Web Directories\n\n"
            for directory in web_dirs:
                details += f"- {directory}\n"
            details += "\n"
        
        return details

def setup_environment():
    """Setup and validate the environment for the orchestrator"""
    print("Cybersecurity Operations Orchestrator - Environment Setup")
    print("=" * 60)
    
    # Check Python version
    import sys
    if sys.version_info < (3, 6):
        print("ERROR: Python 3.6+ is required")
        return False
    
    print(f"✓ Python version: {sys.version}")
    
    # Check tool availability
    print("\nChecking tool availability:")
    tool_status = Config.validate_tools()
    
    all_tools_available = True
    for tool, available in tool_status.items():
        status = "✓" if available else "✗"
        print(f"{status} {tool}: {'Available' if available else 'Not found'}")
        if not available:
            all_tools_available = False
    
    if not all_tools_available:
        print("\nWARNING: Some tools are not available. The orchestrator may not function optimally.")
        print("Please install missing tools for full functionality.")
    
    # Check wordlists
    print(f"\nWordlist check:")
    wordlist = Config.get_wordlist("directories")
    if os.path.exists(wordlist):
        print(f"✓ Directory wordlist: {wordlist}")
    else:
        print(f"✗ Directory wordlist not found: {wordlist}")
        print("Consider downloading SecLists or other wordlist collections.")
    
    return True

if __name__ == "__main__":
    setup_environment()
