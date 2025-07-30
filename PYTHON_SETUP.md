# 🚨 Python Not Found - Installation Guide

## The Issue
The error "streamlit is not recognised" occurs because Python is not installed or not properly configured on your system.

## ✅ Solution: Install Python

### Step 1: Download Python
1. Go to **[python.org/downloads](https://python.org/downloads/)**
2. Click **"Download Python 3.12.x"** (latest version)
3. **Save the installer** to your Downloads folder

### Step 2: Install Python
1. **Run the installer** (.exe file)
2. **⚠️ IMPORTANT**: Check **"Add Python to PATH"** ✅
3. **⚠️ IMPORTANT**: Check **"Install pip"** ✅
4. Click **"Install Now"**
5. Wait for installation to complete
6. Click **"Close"**

### Step 3: Restart Command Prompt
1. **Close PowerShell/Command Prompt** completely
2. **Open new PowerShell** (press Win+R, type `powershell`, Enter)
3. Navigate back to project: `cd "d:\Jayant\generate_testcases"`

### Step 4: Verify Installation
```powershell
python --version
# Should show: Python 3.12.x

pip --version
# Should show: pip 24.x.x
```

### Step 5: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 6: Run the Application
```powershell
streamlit run streamlit_app.py
```

## 🔄 Alternative: Use Python from Microsoft Store

If the above doesn't work:

1. Open **Microsoft Store**
2. Search for **"Python 3.12"**
3. Click **"Get"** to install
4. Restart PowerShell
5. Run: `python --version`

## 🆘 Still Not Working?

### Option 1: Use Full Path
Find where Python installed (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python312\`)

```powershell
# Use full path
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe --version
C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts\pip.exe install -r requirements.txt
```

### Option 2: Add to PATH Manually
1. Search "Environment Variables" in Windows
2. Click "Environment Variables" button
3. Under "System Variables", find "Path"
4. Click "Edit"
5. Click "New" and add: `C:\Users\YourName\AppData\Local\Programs\Python\Python312\`
6. Click "New" and add: `C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts\`
7. Click "OK" on all dialogs
8. Restart PowerShell

## ✅ After Python is Installed

Run these commands in order:

```powershell
# 1. Verify Python
python --version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up AI provider (choose one):

# Option A: Groq (Free)
# Edit .env file and add: GROQ_API_KEY=your_key_from_groq.com

# Option B: Ollama (Free, Local)
# Download from ollama.ai, then run:
# ollama pull llama3.2
# ollama serve

# 4. Run the web app
streamlit run streamlit_app.py

# 5. Open browser to: http://localhost:8501
```

## 🎯 Quick Test

Once Python is installed, test with this simple command:
```powershell
python -c "print('Python is working!')"
```

If you see "Python is working!", you're ready to proceed!

---

**Next Step**: After installing Python, run `pip install -r requirements.txt` to install Streamlit and other dependencies.
