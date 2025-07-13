@echo off
echo Testing COO Environment...
python examples.py check-deps
echo.
echo To run a dry-run test:
echo python examples.py dry-run
echo.
echo To run the actual orchestrator:
echo python orchestrator.py --target TARGET_IP --groq-api-key YOUR_KEY
pause
