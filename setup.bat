@echo off
REM Cybersecurity Operations Orchestrator - Setup Script for Windows
REM This script helps set up the environment on Windows systems

echo.
echo 🔧 Cybersecurity Operations Orchestrator Setup for Windows
echo ================================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo ✓ pip is available

REM Install Python dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✓ Python dependencies installed

REM Create directories
echo.
echo Creating directories...
if not exist "wordlists" mkdir wordlists
if not exist "pentest_results" mkdir pentest_results

REM Create sample wordlist
if not exist "wordlists\common.txt" (
    echo Creating sample wordlist...
    (
        echo admin
        echo administrator
        echo login
        echo test
        echo backup
        echo config
        echo uploads
        echo images
        echo js
        echo css
        echo api
        echo v1
        echo v2
        echo old
        echo tmp
        echo temp
        echo logs
        echo data
        echo files
        echo docs
        echo downloads
        echo index
        echo home
        echo about
        echo contact
    ) > wordlists\common.txt
    echo ✓ Created sample wordlist: wordlists\common.txt
)

REM Create sample configuration
echo.
echo Creating sample configuration...
(
    echo # Sample configuration for COO on Windows
    echo # Copy this file to config.bat and customize as needed
    echo.
    echo @echo off
    echo.
    echo REM Groq API Configuration
    echo set GROQ_API_KEY=your_groq_api_key_here
    echo.
    echo REM Default target ^(can be overridden via command line^)
    echo set DEFAULT_TARGET=192.168.1.100
    echo.
    echo REM Tool paths ^(customize if tools are not in PATH^)
    echo set NMAP_PATH=nmap
    echo set GOBUSTER_PATH=gobuster
    echo set DIRB_PATH=dirb
    echo set NIKTO_PATH=nikto
    echo set SQLMAP_PATH=sqlmap
    echo.
    echo REM Wordlist paths
    echo set WORDLIST_DIR=wordlists
    echo set COMMON_WORDLIST=%%WORDLIST_DIR%%\common.txt
    echo.
    echo REM Output configuration
    echo set OUTPUT_DIR=pentest_results
    echo set MAX_ITERATIONS=50
    echo.
    echo echo Configuration loaded successfully
) > sample_config.bat

echo ✓ Created sample_config.bat

REM Check for penetration testing tools
echo.
echo Checking for penetration testing tools...

REM Check nmap
nmap --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ nmap is available
) else (
    echo ✗ nmap is not available
    echo   Download from: https://nmap.org/download.html
)

REM Check curl
curl --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ curl is available
) else (
    echo ✗ curl is not available ^(usually included with Windows 10+^)
)

REM Check other tools
set "tools=gobuster dirb nikto sqlmap"
for %%t in (%tools%) do (
    %%t --help >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✓ %%t is available
    ) else (
        echo ✗ %%t is not available
    )
)

echo.
echo Tool Installation Notes for Windows:
echo =====================================
echo.
echo 1. nmap: Download from https://nmap.org/download.html
echo    - Choose "Latest stable release self-installer"
echo    - Make sure to add to PATH during installation
echo.
echo 2. For other tools, consider using:
echo    - Chocolatey: choco install nmap
echo    - WSL (Windows Subsystem for Linux) with Kali Linux
echo    - Docker with Kali Linux container
echo    - Manual installation from GitHub releases
echo.
echo 3. Alternative: Use the orchestrator in a Linux VM or WSL

REM Create a quick test script
echo.
echo Creating test script...
(
    echo @echo off
    echo echo Testing COO Environment...
    echo python examples.py check-deps
    echo echo.
    echo echo To run a dry-run test:
    echo echo python examples.py dry-run
    echo echo.
    echo echo To run the actual orchestrator:
    echo echo python orchestrator.py --target TARGET_IP --groq-api-key YOUR_KEY
    echo pause
) > test_environment.bat

echo ✓ Created test_environment.bat

echo.
echo Setup completed!
echo ================
echo.
echo Next steps:
echo 1. Get your Groq API key from: https://console.groq.com/
echo 2. Edit sample_config.bat with your API key and settings
echo 3. Install penetration testing tools (see notes above)
echo 4. Run: python orchestrator.py --target TARGET_IP --groq-api-key YOUR_KEY
echo.
echo For testing: python examples.py dry-run
echo Or run: test_environment.bat
echo.
echo ⚠️  IMPORTANT: Only test systems you own or have explicit permission to test!
echo.
pause
