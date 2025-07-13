@echo off
echo.
echo ============================================================
echo   Cybersecurity Operations Orchestrator (COO)
echo   Quick Start Guide
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python is available
echo.

REM Show available commands
echo Available commands:
echo.
echo 1. Setup Environment:
echo    setup.bat
echo.
echo 2. Test Environment:
echo    python examples.py check-deps
echo.
echo 3. Run Dry Test:
echo    python examples.py dry-run
echo.
echo 4. Create Test Environment:
echo    python examples.py test-env
echo.
echo 5. Generate Sample Config:
echo    python examples.py sample-config
echo.
echo 6. Run Actual Penetration Test:
echo    python orchestrator.py --target TARGET_IP --groq-api-key YOUR_API_KEY
echo.
echo ============================================================
echo.

REM Ask user what they want to do
echo What would you like to do?
echo [1] Run setup
echo [2] Check dependencies
echo [3] Run dry test
echo [4] Show help
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Running setup...
    call setup.bat
) else if "%choice%"=="2" (
    echo.
    echo Checking dependencies...
    python examples.py check-deps
) else if "%choice%"=="3" (
    echo.
    echo Running dry test...
    python examples.py dry-run
) else if "%choice%"=="4" (
    echo.
    echo Opening documentation...
    start README.md
) else if "%choice%"=="5" (
    echo.
    echo Goodbye!
    exit /b 0
) else (
    echo.
    echo Invalid choice. Please run the script again.
)

echo.
pause
