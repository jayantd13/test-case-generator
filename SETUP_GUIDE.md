# 🧪 Test Case Generator - Complete Setup Guide

## 📋 What This Tool Does

This tool automatically generates comprehensive test cases from JIRA ticket details using AI. You provide:
- **JIRA Ticket Number** (e.g., AUTH-101)
- **Priority** (High, Medium, Low)
- **Acceptance Criteria** (detailed requirements)

The AI generates multiple test cases covering:
- ✅ Happy path scenarios
- ⚠️ Edge cases
- ❌ Negative test scenarios
- 🔍 Boundary conditions

## 🚀 Quick Start (Windows)

### Step 1: Install Python
1. Go to [python.org](https://python.org/downloads/)
2. Download Python 3.8+ for Windows
3. **Important**: Check "Add Python to PATH" during installation
4. Restart your command prompt/PowerShell

### Step 2: Install Dependencies
```powershell
# Navigate to project folder
cd "d:\Jayant\generate_testcases"

# Install required packages
pip install -r requirements.txt
```

### Step 3: Choose AI Provider

#### Option A: Groq (Recommended - Free Tier)
1. Visit [groq.com](https://groq.com) and create account
2. Get your free API key
3. Edit `.env` file:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

#### Option B: Ollama (Completely Free, Local)
1. Download from [ollama.ai](https://ollama.ai)
2. Install and run:
   ```powershell
   # Install a model
   ollama pull llama3.2
   
   # Start service
   ollama serve
   ```

### Step 4: Run the Tool

#### Web Interface (Easiest):
```powershell
streamlit run streamlit_app.py
```
Then open `http://localhost:8501` in your browser.

#### Command Line:
```powershell
python test_case_generator.py --jira "PROJ-123" --priority "High" --criteria "User should be able to login with valid credentials"
```

## 🎯 Usage Examples

### Example 1: Login Feature
```powershell
python test_case_generator.py \
  --jira "AUTH-101" \
  --priority "High" \
  --criteria "User login with email/password. Valid credentials redirect to dashboard. Invalid credentials show error message." \
  --component "Authentication"
```

### Example 2: API Testing
```powershell
python test_case_generator.py \
  --jira "API-205" \
  --priority "Medium" \
  --criteria "GET /users/{id} returns user data with valid token. Returns 401 for invalid token. Returns 404 for non-existent user." \
  --test-type "API"
```

## 📊 Generated Output

The tool creates Excel files with columns matching your template:
- Test Key (AUTO-101-TC-001)
- Title (Verify successful login with valid credentials)
- Preconditions (User account exists and is active)
- Test Steps (Detailed step-by-step instructions)
- Expected Results (Expected outcomes)
- Plus all other template columns

## 🔧 Configuration

Edit `.env` file to customize:
```env
# AI Provider (groq or ollama)
DEFAULT_AI_PROVIDER=groq
DEFAULT_MODEL=llama3-8b-8192

# Default values for test cases
DEFAULT_TEST_TYPE=Functional
DEFAULT_COMPONENT=Web Application
DEFAULT_RELEASE=1.0
DEFAULT_TEST_STATUS=Draft
DEFAULT_AUTOMATION_STATUS=Not Automated
```

## 💡 Tips for Better Results

### ✅ Good Acceptance Criteria:
```
Login Functionality:
- User enters valid email and password
- System validates credentials against database
- Valid login redirects to dashboard with welcome message
- Invalid login shows "Invalid email or password" error
- Empty fields show validation messages
- Forgot password link opens reset form
- Remember me keeps user logged in for 30 days
```

### ❌ Poor Acceptance Criteria:
```
User should be able to login
```

## 🆘 Troubleshooting

### "Python was not found"
- Install Python from python.org
- Make sure "Add to PATH" was checked
- Restart command prompt

### "GROQ_API_KEY not found"
- Get API key from groq.com
- Add to .env file: `GROQ_API_KEY=your_key`
- Restart the application

### "Error calling Ollama API"
- Install Ollama from ollama.ai
- Run: `ollama pull llama3.2`
- Start: `ollama serve`

### Poor Quality Test Cases
- Provide more detailed acceptance criteria
- Include specific scenarios and data requirements
- Use "Given-When-Then" format

## 📁 Project Structure
```
generate_testcases/
├── test_case_generator.py    # Core generator logic
├── streamlit_app.py         # Web interface
├── requirements.txt         # Python dependencies
├── .env                     # Configuration
├── README.md               # This guide
├── examples.py             # Example usage
├── setup.bat              # Windows setup script
└── Testcases_template.xlsx # Excel template
```

## 🎉 Success!

Once set up, you can generate test cases in seconds:
1. 🌐 **Web**: Run `streamlit run streamlit_app.py` → Open browser
2. 💻 **CLI**: Run `python test_case_generator.py --help`
3. 📥 **Download**: Get Excel files with your generated test cases

Happy testing! 🧪
