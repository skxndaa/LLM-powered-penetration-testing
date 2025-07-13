#!/usr/bin/env python3
"""
Cybersecurity Operations Orchestrator (COO)
A Python orchestrator that interfaces with Groq LLM API to conduct automated penetration testing.
"""

import argparse
import json
import subprocess
import time
import os
import sys
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import requests
from pathlib import Path

class CybersecOrchestrator:
    def __init__(self, groq_api_key: str, target_ip: str, output_dir: str = "pentest_results"):
        self.groq_api_key = groq_api_key
        self.target_ip = target_ip
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize state
        self.state = {
            "target_ip": target_ip,
            "open_ports": [],
            "vulnerabilities": [],
            "web_directories": [],
            "notes": "Penetration test initialized"
        }
        
        # Setup logging
        self.setup_logging()
        
        # Groq API configuration
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-70b-8192"  # Current Groq model
        
        # Track session
        self.session_start = datetime.now()
        self.command_count = 0
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.output_dir / f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_system_prompt(self) -> str:
        """Return the master system prompt for the LLM"""
        return '''You are "COO" (Cybersecurity Operations Orchestrator), an expert-level penetration tester and AI assistant, running on the high-speed Groq platform. Your primary function is to direct a network penetration test by processing data, generating tool commands, and analyzing outputs in a structured, step-by-step manner. Your speed is a key asset, so provide analysis and the next command as quickly as possible.

**Your Core Directives:**

1. **Stateless Operation:** You operate one step at a time. You will be given the current "state" of the pentest (what has been found so far) and the output of the last tool you ran. Your task is to analyze this new information and decide on the single best next action.

2. **Structured I/O:** You MUST communicate exclusively in JSON format. The Groq API will be used to parse this structured output. Do not provide any conversational text, apologies, or explanations outside of the specified JSON structure.

3. **Command Generation:** You will generate precise, single-line commands for a predefined set of cybersecurity tools. You do not execute these commands yourself; you provide them to an external orchestrator.

4. **Tool Knowledge:** You are an expert in the use of the following tools: `nmap`, `gobuster`, `dirb`, `nikto`, `whatweb`, `sqlmap`, `searchsploit`, and `msfconsole`. You understand their flags, syntax, and typical outputs.

5. **Analysis and Synthesis:** Your most important task is to analyze the output of tools. Identify open ports, services, versions, potential vulnerabilities, interesting directories, and other attack vectors. You must update the state with your findings.

6. **Pentesting Methodology:** You will follow a standard methodology:
   a. **Initial Reconnaissance:** Start with broad, non-intrusive scans.
   b. **Enumeration:** Dig deeper into discovered services (e.g., web directories, user enumeration).
   c. **Vulnerability Identification:** Correlate service/version information with known vulnerabilities.
   d. **Exploitation Suggestion:** Suggest specific exploits or methods to test vulnerabilities. You will not execute them, but provide the precise commands for the orchestrator to do so.
   e. **Reporting:** At the end of the process, you will summarize all findings into a coherent report.

**JSON I/O Specification:**

**Input JSON (from Orchestrator to you):**
{
  "state": {
    "target_ip": "...",
    "open_ports": [
      {"port": 22, "service": "ssh", "version": "..."},
      {"port": 80, "service": "http", "version": "..."}
    ],
    "vulnerabilities": [
      {"cve": "...", "description": "...", "port": 80}
    ],
    "web_directories": ["/admin", "/login"],
    "notes": "..."
  },
  "last_tool_output": "..." // Raw text output from the last executed command
}

**Output JSON (from you to Orchestrator):**
{
  "analysis": "A brief, expert analysis of the last_tool_output and its implications. What did we learn? What does it mean?",
  "next_command": "The single, complete, and precise command to execute next. Example: 'nmap -sV -p 80,443 -oN nmap_service_scan 192.168.1.10'",
  "updated_state": {
    // The full, updated state object reflecting your new analysis.
    // You must merge your new findings with the previous state.
  },
  "final_report": null // Or a string containing a full Markdown report if next_command is "COMPLETE"
}

You must respond ONLY with valid JSON. No additional text, explanations, or formatting outside the JSON structure.'''

    def call_groq_api(self, user_message: str) -> Dict[str, Any]:
        """Make API call to Groq LLM"""
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.1,  # Low temperature for consistent, focused responses
            "max_tokens": 2048
        }
        
        try:
            self.logger.info("Sending request to Groq API...")
            response = requests.post(self.groq_api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            llm_response = result['choices'][0]['message']['content']
            
            self.logger.info(f"Received response from Groq API: {len(llm_response)} characters")
            return json.loads(llm_response)
            
        except requests.exceptions.RequestException as e:
            if "429" in str(e) or "Too Many Requests" in str(e):
                self.logger.warning("API rate limit hit. Waiting 30 seconds before retry...")
                time.sleep(30)
                # Retry once
                try:
                    response = requests.post(self.groq_api_url, headers=headers, json=payload, timeout=30)
                    response.raise_for_status()
                    result = response.json()
                    llm_response = result['choices'][0]['message']['content']
                    self.logger.info(f"Retry successful after rate limit")
                    return json.loads(llm_response)
                except Exception as retry_error:
                    self.logger.error(f"Retry also failed: {retry_error}")
                    raise
            else:
                self.logger.error(f"API request failed: {e}")
                raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response as JSON: {e}")
            self.logger.error(f"Raw response: {llm_response}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in API call: {e}")
            raise

    def execute_command(self, command: str) -> str:
        """Execute a shell command and return its output"""
        self.command_count += 1
        command_file = self.output_dir / f"command_{self.command_count:03d}.txt"
        output_file = self.output_dir / f"output_{self.command_count:03d}.txt"
        
        # Save the command
        with open(command_file, 'w') as f:
            f.write(f"Command #{self.command_count}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Command: {command}\n")
        
        self.logger.info(f"Executing command #{self.command_count}: {command}")
        
        try:
            # Execute command
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=300  # 5 minute timeout
                )
            else:  # Unix-like
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=300
                )
            
            # Combine stdout and stderr
            output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nRETURN CODE: {result.returncode}"
            
            # Save output
            with open(output_file, 'w') as f:
                f.write(output)
            
            self.logger.info(f"Command completed with return code: {result.returncode}")
            return output
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after 300 seconds"
            self.logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Command execution failed: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

    def create_input_json(self, last_tool_output: str = "") -> str:
        """Create the input JSON for the LLM"""
        input_data = {
            "state": self.state,
            "last_tool_output": last_tool_output
        }
        return json.dumps(input_data, indent=2)

    def save_session_state(self, llm_response: Dict[str, Any]):
        """Save the current session state"""
        session_file = self.output_dir / "session_state.json"
        session_data = {
            "session_start": self.session_start.isoformat(),
            "command_count": self.command_count,
            "current_state": self.state,
            "last_response": llm_response
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

    def run_penetration_test(self, max_iterations: int = 50):
        """Main orchestration loop"""
        self.logger.info(f"Starting penetration test against {self.target_ip}")
        self.logger.info(f"Results will be saved to: {self.output_dir}")
        
        last_tool_output = ""
        
        for iteration in range(max_iterations):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"ITERATION {iteration + 1}")
            self.logger.info(f"{'='*60}")
            
            try:
                # Create input for LLM
                input_json = self.create_input_json(last_tool_output)
                
                # Get LLM response
                llm_response = self.call_groq_api(input_json)
                
                # Save session state
                self.save_session_state(llm_response)
                
                # Log LLM analysis
                self.logger.info(f"LLM Analysis: {llm_response.get('analysis', 'No analysis provided')}")
                
                # Check if test is complete
                next_command = llm_response.get('next_command', '')
                if next_command == "COMPLETE":
                    self.logger.info("LLM indicated test completion")
                    final_report = llm_response.get('final_report')
                    if final_report:
                        report_file = self.output_dir / "final_report.md"
                        with open(report_file, 'w') as f:
                            f.write(final_report)
                        self.logger.info(f"Final report saved to: {report_file}")
                    break
                
                # Update state
                if 'updated_state' in llm_response:
                    self.state = llm_response['updated_state']
                
                # Execute the next command
                if next_command:
                    last_tool_output = self.execute_command(next_command)
                    
                    # Longer pause to avoid API rate limiting
                    time.sleep(3)  # Increased from 1 to 3 seconds
                else:
                    self.logger.warning("No command provided by LLM")
                    break
                    
            except Exception as e:
                self.logger.error(f"Error in iteration {iteration + 1}: {e}")
                break
        
        else:
            self.logger.warning(f"Maximum iterations ({max_iterations}) reached")
        
        self.logger.info("Penetration test completed")
        self.logger.info(f"Total commands executed: {self.command_count}")
        self.logger.info(f"Session duration: {datetime.now() - self.session_start}")

def main():
    parser = argparse.ArgumentParser(description="Cybersecurity Operations Orchestrator")
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--groq-api-key", help="Groq API key (or set GROQ_API_KEY env variable)")
    parser.add_argument("--output-dir", default="pentest_results", help="Output directory for results")
    parser.add_argument("--max-iterations", type=int, default=50, help="Maximum number of iterations")
    parser.add_argument("--save-api-key", help="Save API key to config file for future use")
    
    args = parser.parse_args()
    
    # Handle API key saving
    if args.save_api_key:
        from config import Config
        Config.save_groq_api_key(args.save_api_key)
        print("API key saved. You can now run without --groq-api-key parameter.")
        return
    
    # Get API key from various sources
    from config import Config
    groq_api_key = args.groq_api_key or Config.get_groq_api_key()
    
    if not groq_api_key:
        print("Error: No Groq API key provided!")
        print("Options:")
        print("1. Use --groq-api-key parameter")
        print("2. Set GROQ_API_KEY environment variable")
        print("3. Save key to config: python orchestrator.py --save-api-key YOUR_KEY")
        print("4. Create groq_config.json file with your key")
        sys.exit(1)
    
    # Validate target IP format (basic check)
    import ipaddress
    try:
        ipaddress.ip_address(args.target)
    except ValueError:
        print(f"Error: Invalid IP address format: {args.target}")
        sys.exit(1)
    
    # Create orchestrator and run
    orchestrator = CybersecOrchestrator(
        groq_api_key=groq_api_key,
        target_ip=args.target,
        output_dir=args.output_dir
    )
    
    try:
        orchestrator.run_penetration_test(max_iterations=args.max_iterations)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
