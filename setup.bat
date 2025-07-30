@echo off
echo 🧪 Test Case Generator - Quick Setup
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Install dependencies
echo 📦 Installing Python dependencies...
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully!
) else (
    echo ❌ Failed to install dependencies. Please check your Python installation.
    pause
    exit /b 1
)

REM Check for .env file
if not exist .env (
    echo ⚠️  .env file not found. Please edit the .env file with your API keys
)

echo.
echo 🚀 Setup complete! You can now:
echo    1. Web Interface: streamlit run streamlit_app.py
echo    2. Command Line: python test_case_generator.py --help
echo.
echo 📖 Read README.md for detailed instructions
pause
