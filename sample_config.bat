# Sample configuration for COO on Windows
# Copy this file to config.bat and customize as needed

@echo off

REM Groq API Configuration
set GROQ_API_KEY=your_groq_api_key_here

REM Default target (can be overridden via command line)
set DEFAULT_TARGET=192.168.1.100

REM Tool paths (customize if tools are not in PATH)
set NMAP_PATH=nmap
set GOBUSTER_PATH=gobuster
set DIRB_PATH=dirb
set NIKTO_PATH=nikto
set SQLMAP_PATH=sqlmap

REM Wordlist paths
set WORDLIST_DIR=wordlists
set COMMON_WORDLIST=%WORDLIST_DIR%\common.txt

REM Output configuration
set OUTPUT_DIR=pentest_results
set MAX_ITERATIONS=50

echo Configuration loaded successfully
