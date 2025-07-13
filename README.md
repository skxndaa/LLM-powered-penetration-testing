# Cybersecurity Operations Orchestrator (COO)

An intelligent LLM-powered penetration testing orchestrator that combines the analytical power of Groq's high-speed language models with traditional cybersecurity tools to conduct automated penetration tests.

## 🏗️ Architecture Overview

The system follows a three-tier architecture:

1. **The LLM (The "Brain")** - Groq-powered AI that acts as an expert pentester, deciding which tools to use and how to interpret results
2. **The Orchestrator (The "Hands")** - Python script that executes commands and manages the workflow  
3. **The Tools (The "Toolbelt")** - Standard pentesting tools like nmap, gobuster, nikto, etc.

## 🚀 Features

- **Intelligent Decision Making**: LLM analyzes scan results and determines the next logical step
- **Structured Workflow**: Follows standard pentesting methodology (Reconnaissance → Enumeration → Vulnerability Assessment → Exploitation)
- **JSON-Based Communication**: Structured API communication for reliable automation
- **Comprehensive Logging**: Detailed logs and session state tracking
- **Automated Reporting**: Generates markdown reports with findings and recommendations
- **High-Speed Analysis**: Leverages Groq's optimized inference for rapid response times
- **Interactive Web Interface**: Sleek black-and-red dashboard to start/stop scans, view live findings, and generate reports
- **One-Click PDF Reports**: Produces a polished, brand-ready PDF with executive summary, findings, and statistics

## 📋 Prerequisites

### Required Tools
The orchestrator expects the following tools to be available in your system PATH:

- `nmap` - Network discovery and security auditing
- `gobuster` - Directory/file & DNS busting tool  
- `dirb` - Web content scanner
- `nikto` - Web server scanner
- `whatweb` - Web application fingerprinter
- `sqlmap` - SQL injection testing tool
- `searchsploit` - Exploit database search
- `msfconsole` - Metasploit framework console

### API Requirements
- **Groq API Key**: Get your API key from [Groq Console](https://console.groq.com/)

## ⚙️ API Key Configuration

You have several options to configure your Groq API key:

### Option 1: Interactive Setup (Recommended)
```powershell
python setup_api_key.py
```
This script will guide you through the process and let you choose how to store your key.

### Option 2: Save via Command Line
```powershell
python orchestrator.py --save-api-key "your_groq_api_key_here"
```

### Option 3: Environment Variable
```powershell
# PowerShell
$env:GROQ_API_KEY = "your_groq_api_key_here"

# Command Prompt
set GROQ_API_KEY=your_groq_api_key_here
```

### Option 4: Direct Parameter (Less Secure)
```powershell
python orchestrator.py --target 192.168.1.100 --groq-api-key "your_groq_api_key_here"
```

## 🛠️ Installation

1. **Clone or download the project**:
   ```powershell
   # If you have the files locally
   cd c:\Users\rexjo\soc_gen
   ```

2. **Install Python dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install cybersecurity tools** (examples for different platforms):

   **Kali Linux / Debian**:
   ```bash
   sudo apt update
   sudo apt install nmap gobuster dirb nikto whatweb sqlmap exploitdb metasploit-framework
   ```

   **Windows (using Chocolatey)**:
   ```powershell
   choco install nmap
   # Additional tools may require manual installation
   ```

   **macOS (using Homebrew)**:
   ```bash
   brew install nmap gobuster dirb nikto
   ```

## 🖥️ Web Interface Quick-Start

1. Install extra dependencies:
   ```powershell
   pip install flask flask_cors reportlab
   ```
2. Launch the server:
   ```powershell
   python web_interface/app.py
   ```
3. Open a browser to `http://127.0.0.1:5000`, set the target IP, then click **Start Scan**. After completion, hit **Generate Report** to download the PDF.

---

## 🎯 CLI Usage

### Quick Start

1. **Configure your API key** (choose one method):
   ```powershell
   # Interactive setup (recommended)
   python setup_api_key.py
   
   # Or save directly
   python orchestrator.py --save-api-key "your_groq_api_key_here"
   
   # Or set environment variable
   $env:GROQ_API_KEY = "your_groq_api_key_here"
   ```

2. **Run the orchestrator**:
   ```powershell
   python orchestrator.py --target 192.168.1.100
   ```

### Basic Usage

```powershell
# If API key is configured
python orchestrator.py --target 192.168.1.100

# Or specify key directly
python orchestrator.py --target 192.168.1.100 --groq-api-key YOUR_GROQ_API_KEY
```

### Advanced Options

```powershell
python orchestrator.py \
  --target 10.10.11.123 \
  --groq-api-key YOUR_GROQ_API_KEY \
  --output-dir custom_results \
  --max-iterations 30
```

### Parameters

- `--target`: Target IP address (required)
- `--groq-api-key`: Your Groq API key (required)
- `--output-dir`: Directory for saving results (default: "pentest_results")
- `--max-iterations`: Maximum number of analysis iterations (default: 50)

## 📊 Output Structure

The orchestrator creates a comprehensive output directory:

```
pentest_results/
├── orchestrator_YYYYMMDD_HHMMSS.log    # Detailed execution log
├── session_state.json                   # Current session state
├── final_report.md                      # Final penetration test report
├── command_001.txt                      # Individual command records
├── output_001.txt                       # Tool output files
├── command_002.txt
├── output_002.txt
└── ...
```

## 🔄 Workflow Example

1. **Initialization**: Target IP provided, LLM receives empty state
2. **Reconnaissance**: LLM decides to run `nmap -F --open -oN nmap_fast_scan 192.168.1.100`
3. **Service Enumeration**: Analyzes port scan results, runs detailed service detection
4. **Web Discovery**: If web services found, enumerates directories with gobuster
5. **Vulnerability Assessment**: Correlates findings with known vulnerabilities
6. **Exploitation Guidance**: Suggests specific exploits or attack vectors
7. **Reporting**: Compiles comprehensive markdown report

## 🧠 LLM Behavior

The LLM follows a structured JSON communication protocol:

**Input Format**:
```json
{
  "state": {
    "target_ip": "192.168.1.100",
    "open_ports": [...],
    "vulnerabilities": [...],
    "web_directories": [...],
    "notes": "..."
  },
  "last_tool_output": "Raw command output..."
}
```

**Output Format**:
```json
{
  "analysis": "Expert analysis of the results...",
  "next_command": "nmap -sV -p 80,443 192.168.1.100",
  "updated_state": { ... },
  "final_report": null
}
```

## ⚠️ Important Notes

### Legal and Ethical Usage
- **Only test systems you own or have explicit permission to test**
- This tool is for authorized security testing and educational purposes only
- Unauthorized penetration testing may be illegal in your jurisdiction

### Security Considerations
- Store your Groq API key securely (consider environment variables)
- Review generated commands before running in production environments
- Be mindful of network noise and detection by security systems

### Limitations
- The LLM provides guidance but doesn't execute actual exploits
- Some manual verification of findings may still be required
- Tool availability and versions may affect command execution

## 🔧 Configuration

### Environment Variables (Optional)
```powershell
# Set your API key as an environment variable
$env:GROQ_API_KEY="your_api_key_here"

# Then run without --groq-api-key flag
python orchestrator.py --target 192.168.1.100
```

### Customizing Tool Paths
If tools are not in your PATH, you can modify the command generation in the script or create wrapper scripts.

## 🤝 Contributing

This is a foundational implementation that can be extended with:
- Additional tool integrations
- Custom vulnerability databases
- Integration with other AI models
- Enhanced reporting formats
- Web interface for easier operation

## 📜 License

This project is for educational and authorized security testing purposes. Use responsibly and in compliance with applicable laws and regulations.

## 🆘 Troubleshooting

### Common Issues

1. **"Command not found" errors**: Ensure all required tools are installed and in PATH
2. **API errors**: Verify your Groq API key is valid and has sufficient credits
3. **Permission errors**: Run with appropriate privileges for network scanning
4. **Timeout issues**: Some commands may need longer timeout values for larger networks

### Debug Mode
Add logging level configuration for verbose output:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues related to:
- **Groq API**: Check [Groq Documentation](https://console.groq.com/docs)
- **Tool installation**: Refer to individual tool documentation
- **Network issues**: Verify target accessibility and permissions

---

**Remember**: Always obtain proper authorization before conducting any security testing!
