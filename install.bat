@echo off
echo.
echo 🧪 Test Case Generator - Python Setup Check
echo ============================================
echo.

REM Check if Python is installed
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is NOT installed or not in PATH
    echo.
    echo 🚀 SOLUTION:
    echo 1. Go to: https://python.org/downloads/
    echo 2. Download Python 3.12.x
    echo 3. ⚠️  IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Restart this script after installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed:
python --version
echo.

REM Check if pip is available
echo Checking for pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo ✅ pip is available:
pip --version
echo.

REM Install dependencies
echo 📦 Installing Python packages...
echo This may take a few minutes...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ All dependencies installed successfully!
    echo.
    echo 🎉 Setup Complete! You can now:
    echo.
    echo 1. 🌐 Web Interface:
    echo    streamlit run streamlit_app.py
    echo    Then open: http://localhost:8501
    echo.
    echo 2. 💻 Command Line:
    echo    python test_case_generator.py --help
    echo.
    echo 3. 📖 Read SETUP_GUIDE.md for detailed instructions
    echo.
) else (
    echo.
    echo ❌ Failed to install dependencies
    echo.
    echo Possible solutions:
    echo 1. Check internet connection
    echo 2. Run as Administrator
    echo 3. Try: python -m pip install --upgrade pip
    echo.
)

pause
