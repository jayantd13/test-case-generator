# Test Case Generator

A Python-based tool for automatically generating comprehensive test cases from JIRA ticket details using AI models. The tool reads your Excel template and generates detailed test cases based on JIRA ticket number, priority, and acceptance criteria.

## Features

- 🤖 **AI-Powered Generation**: Uses free AI models (Groq, Gemini, Ollama) to generate comprehensive test cases
- 📊 **Excel Integration**: Reads from and writes to Excel templates matching your existing format
- 📁 **Organized Output**: Generated test cases are automatically saved to the `testcases/` folder
- 📜 **History Tracking**: Complete history of all generated test cases with search and download capabilities
- 🎯 **Multiple Test Scenarios**: Generates happy path, edge cases, negative scenarios, and boundary conditions
- 🌐 **Web Interface**: Beautiful Streamlit web app with navigation and history management
- 💻 **Command Line**: CLI tool for automation and scripting
- 🆓 **Free Options**: Supports completely free AI providers

## Supported AI Providers

### 1. Groq (Recommended)
- **Cost**: Free tier available (fast and reliable)
- **Setup**: Get API key from [groq.com](https://groq.com)
- **Models**: llama3-8b-8192, mixtral-8x7b-32768

### 2. Google Gemini
- **Cost**: Free tier available (Google's AI model)
- **Setup**: Get API key from [makersuite.google.com](https://makersuite.google.com/app/apikey)
- **Models**: gemini-1.5-flash, gemini-1.5-pro

### 3. Ollama 
- **Cost**: Completely free (runs locally)
- **Setup**: Install from [ollama.ai](https://ollama.ai)
- **Models**: llama3.2, codellama, mistral, etc.

## Installation

1. **Clone or download** this project to your computer

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AI Provider** (choose one):

   ### Option A: Groq (Cloud-based, Free tier)
   ```bash
   # Get free API key from groq.com
   # Edit .env file and add:
   GROQ_API_KEY=your_groq_api_key_here
   ```

   ### Option B: Google Gemini (Cloud-based, Free tier)
   ```bash
   # Get free API key from makersuite.google.com
   # Edit .env file and add:
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   ### Option C: Ollama (Local, Completely free)
   ```bash
   # Install Ollama
   # Download a model
   ollama pull llama3.2
   
   # Start Ollama service
   ollama serve
   ```

## Usage

### Web Interface (Recommended)

1. **Start the web app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open browser** to `http://localhost:8501`

3. **Navigate between pages**:
   - **🚀 Generate Test Cases**: Create new test cases from JIRA tickets
   - **📜 History**: View and download previously generated test cases
   - **ℹ️ About**: Information about the tool

4. **Fill in the form**:
   - JIRA ticket number
   - Priority level
   - Detailed acceptance criteria
   - Select AI provider
   - Generate test cases

5. **Download results**: Generated Excel files are automatically saved and available for download
   - JIRA Ticket Number (e.g., PROJ-123)
   - Priority (High, Medium, Low)
   - Acceptance Criteria (detailed description)

4. **Generate and download** your test cases!

### Command Line Interface

```bash
python test_case_generator.py --jira "PROJ-123" --priority "High" --criteria "User should be able to login with valid credentials and be redirected to dashboard" --provider "groq"

# Using Gemini
python test_case_generator.py --jira "PROJ-123" --priority "High" --criteria "User should be able to login with valid credentials and be redirected to dashboard" --provider "gemini"

# Using Ollama
python test_case_generator.py --jira "PROJ-123" --priority "High" --criteria "User should be able to login with valid credentials and be redirected to dashboard" --provider "ollama"
```

#### Parameters:
- `--jira`: JIRA ticket number (required)
- `--priority`: Priority level (required)
- `--criteria`: Acceptance criteria (required)
- `--provider`: AI provider (groq, gemini, or ollama)
- `--template`: Path to Excel template file
- `--output`: Output file name
- `--component`: Component name
- `--release`: Release version

## Excel Template Format

The tool works with Excel files containing these columns:

| Column | Description |
|--------|-------------|
| Test Key | Unique test identifier |
| Title | Test case title |
| Preconditions | Prerequisites for the test |
| Priority | Test priority |
| Test Steps | Step-by-step instructions |
| Data for Steps | Required test data |
| Expected Results | Expected outcomes |
| Jira Story ID | Associated JIRA ticket |
| Test Type | Type of test (Functional, API, etc.) |
| Component | Component being tested |
| Release | Target release |
| Test Case Status | Current status |
| Tags | Test tags |
| Automation Status | Automation readiness |
| Automation Key | Automation identifier |

## Examples

### Example 1: Login Feature
```bash
python test_case_generator.py \
  --jira "AUTH-101" \
  --priority "High" \
  --criteria "User should be able to login with username/password. Valid credentials redirect to dashboard. Invalid credentials show error message." \
  --component "Authentication" \
  --test-type "Functional"
```

### Example 2: API Testing
```bash
python test_case_generator.py \
  --jira "API-205" \
  --priority "Medium" \
  --criteria "API should return user profile data when valid token provided. Should return 401 for invalid token." \
  --test-type "API"
```

## Generated Test Case Examples

**Output Files**: All generated test cases are saved to the `testcases/` folder with the following naming convention:
- **CLI**: `testcases/JIRA-TICKET_testcases.xlsx` 
- **Web UI**: `testcases/JIRA-TICKET_testcases_YYYYMMDD_HHMMSS.xlsx` (with timestamp)

The AI will generate comprehensive test cases like:

**Test Case 1: Valid Login**
- **Title**: Verify successful login with valid credentials
- **Preconditions**: User account exists and is active
- **Test Steps**: 
  1. Navigate to login page
  2. Enter valid username
  3. Enter valid password
  4. Click login button
- **Expected Results**: User is redirected to dashboard

**Test Case 2: Invalid Login**
- **Title**: Verify error message for invalid credentials
- **Preconditions**: Login page is accessible
- **Test Steps**:
  1. Navigate to login page
  2. Enter invalid username/password
  3. Click login button
- **Expected Results**: Error message "Invalid credentials" is displayed

## Configuration

Edit the `.env` file to customize:

```env
# AI Provider Settings
DEFAULT_AI_PROVIDER=groq
DEFAULT_MODEL=llama3-8b-8192

# Default Values
DEFAULT_TEST_TYPE=Functional
DEFAULT_COMPONENT=Web Application
DEFAULT_RELEASE=1.0
DEFAULT_TEST_STATUS=Draft
DEFAULT_AUTOMATION_STATUS=Not Automated
```

## Troubleshooting

### Common Issues:

1. **"GROQ_API_KEY not found"**
   - Make sure you've added your API key to the `.env` file
   - Restart the application after adding the key

2. **"Error calling Ollama API"**
   - Check if Ollama is running: `ollama serve`
   - Verify the model is installed: `ollama list`
   - Try pulling a model: `ollama pull llama3.2`

3. **"Permission denied" on Excel file**
   - Close the Excel file if it's open
   - Check write permissions in the directory

4. **Poor quality test cases**
   - Provide more detailed acceptance criteria
   - Include specific scenarios and expected behaviors
   - Use "Given-When-Then" format

## Tips for Better Results

1. **Write detailed acceptance criteria**:
   ```
   ✅ Good: "User should login with email/password. Valid credentials redirect to dashboard. Invalid credentials show 'Invalid email or password' error. Forgot password link should open reset form."
   
   ❌ Poor: "User login functionality"
   ```

2. **Include edge cases in criteria**:
   - What happens with empty fields?
   - What about special characters?
   - How should the system handle network errors?

3. **Specify data requirements**:
   - Valid email formats
   - Password requirements
   - Expected response times

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool!

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/test-case-generator.git
   cd test-case-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up AI provider**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

4. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

## 🌟 Star This Repository

If you find this tool useful, please ⭐ star this repository to help others discover it!

## 📞 Support

- **Documentation**: Check the [Setup Guide](SETUP_GUIDE.md)
- **Issues**: Report bugs or request features in [GitHub Issues](../../issues)
- **Security**: See [Security Policy](SECURITY.md)
- **Deployment**: See [AWS Deployment Guide](AWS_DEPLOYMENT.md)

## License

This project is open source and available under the MIT License.

## Project Structure

```
generate_testcases/
├── testcases/                 # Generated test case files (auto-created)
│   ├── .gitkeep              # Keeps folder in Git
│   └── *.xlsx                # Generated Excel files
├── test_case_generator.py    # Main CLI script
├── streamlit_app.py          # Web interface
├── Testcases_template.xlsx   # Default Excel template
├── requirements.txt          # Python dependencies
├── .env.example              # Environment configuration template
└── README.md                 # This file
```

**Note**: The `testcases/` folder is automatically created when you first generate test cases. All generated files from both the CLI and web interface are saved here with timestamps to avoid conflicts.
