import sys
import subprocess
import os

def check_python():
    """Check if Python is properly installed"""
    try:
        import sys
        print(f"✅ Python {sys.version} found")
        return True
    except:
        print("❌ Python check failed")
        return False

def install_packages():
    """Install required packages"""
    packages = [
        "pandas>=1.5.0",
        "openpyxl>=3.1.0", 
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "streamlit>=1.28.0",
        "groq>=0.4.0"
    ]
    
    print("📦 Installing packages...")
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def main():
    print("🧪 Test Case Generator - Setup")
    print("=" * 40)
    
    if not check_python():
        print("\n❌ Python is not properly installed!")
        print("\n🚀 Please install Python first:")
        print("1. Go to: https://python.org/downloads/")
        print("2. Download Python 3.8+")
        print("3. ⚠️  Check 'Add Python to PATH' during installation")
        print("4. Restart and run this script again")
        input("\nPress Enter to exit...")
        return
    
    print("\n📦 Installing dependencies...")
    if install_packages():
        print("\n✅ Setup completed successfully!")
        print("\n🎉 You can now run:")
        print("   streamlit run streamlit_app.py")
        print("   (Then open http://localhost:8501)")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
