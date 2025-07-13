# Testing Guide for COO

This guide walks you through testing the Cybersecurity Operations Orchestrator (COO) step by step.

## Prerequisites

1. **Linux/WSL Environment**: COO requires Linux/WSL for pentesting tools
2. **Python 3.8+**: Ensure Python 3 is installed
3. **Groq API Key**: Required for LLM functionality

## Quick Setup Test

### 1. Install Dependencies
```bash
# Run this in WSL/Linux
cd /mnt/c/Users/rexjo/soc_gen
pip3 install -r requirements.txt
```

### 2. Test API Connection
```bash
python3 test_api.py
```

If this fails:
- Set up API key: `python3 setup_api_key.py`
- Or export it: `export GROQ_API_KEY="your-key-here"`

### 3. Test Tool Availability
```bash
# Check that pentesting tools are installed
nmap --version
gobuster version
nikto -Version
```

## Testing Scenarios

### A. Offline Testing (No API Key Required)
```bash
# Run simulation tests
python3 test_orchestrator.py
```

This will simulate a complete pentest without making real API calls.

### B. API Testing (Requires Groq API Key)
```bash
# Test API functionality
python3 test_api.py

# Test orchestrator with safe target (localhost)
python3 orchestrator.py --target 127.0.0.1 --max-iterations 2
```

### C. Full Pentest Simulation
```bash
# Complete simulation with analysis
python3 test_orchestrator.py --full-simulation
```

## Expected Outputs

### Successful API Test
```
🔑 Testing Groq API Connection
========================================
✅ API key loaded: gsk_1234...****
✅ Groq client initialized
🧠 Testing LLM response...
✅ API test successful!
Response: API_TEST_SUCCESS
```

### Successful Tool Check
```
Nmap version 7.80 ( https://nmap.org )
gobuster version 3.1.0
Nikto version 2.1.6
```

### Successful Orchestrator Run
```
🤖 COO: Cybersecurity Operations Orchestrator
============================================
🎯 Target: 127.0.0.1
🧠 LLM Model: llama-3.1-70b-versatile
📊 Max Iterations: 2

=== ITERATION 1 ===
🧠 Analyzing current state and planning next action...
📋 LLM Decision: Starting with fast port scan...
🔧 Executing: nmap -F 127.0.0.1
```

## Troubleshooting

### Common Issues

1. **Import errors**: Run `pip3 install -r requirements.txt`
2. **Missing tools**: Run `./setup_linux.sh` in WSL
3. **API errors**: Check API key with `python3 setup_api_key.py`
4. **Permission errors**: Use `sudo` for tool installation

### Environment Issues

- **Windows PowerShell**: COO requires Linux/WSL for pentesting tools
- **Tool not found**: Ensure `/usr/local/bin` is in your PATH
- **Wordlist missing**: Check `wordlists/` directory exists

## Safe Testing Targets

- `127.0.0.1` (localhost) - Safe for testing
- Your own VM/lab environment
- **Never test on systems you don't own!**

## Next Steps

Once testing is successful:
1. Set up a lab environment (VirtualBox, VMware)
2. Use vulnerable VMs like Metasploitable or DVWA
3. Configure proper network isolation
4. Start with `--max-iterations 3` for controlled testing

## Support

If you encounter issues:
1. Check this guide first
2. Review error messages
3. Ensure proper Linux/WSL setup
4. Verify API key configuration
