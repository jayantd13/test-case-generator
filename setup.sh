#!/bin/bash

echo "🧪 Test Case Generator - Quick Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# Install dependencies
echo "📦 Installing Python dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check your Python installation."
    exit 1
fi

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    cp .env .env.template
    echo "📝 Please edit .env file with your API keys"
fi

echo ""
echo "🚀 Setup complete! You can now:"
echo "   1. Web Interface: streamlit run streamlit_app.py"
echo "   2. Command Line: python test_case_generator.py --help"
echo ""
echo "📖 Read README.md for detailed instructions"
