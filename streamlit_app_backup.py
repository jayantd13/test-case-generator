import streamlit as st
import pandas as pd
import os
from test_case_generator import TestCaseGenerator, TestCaseData
from history_manager import TestCaseHistory
import tempfile
from datetime import datetime

st.set_page_config(
    page_title="Test Case Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation
st.sidebar.title("🧪 Test Case Generator")
page = st.sidebar.radio(
    "Navigate to:",
    ["🚀 Generate Test Cases", "📜 History", "ℹ️ About"],
    index=0
)

def show_generator_page():
    """Show the main test case generation page"""
    
    st.title("🧪 Test Case Generator")
    st.markdown("Generate comprehensive test cases from JIRA ticket details using AI")

    # Sidebar for configuration
    st.sidebar.header("Configuration")

    # AI Provider selection
    provider = st.sidebar.selectbox(
        "Select AI Provider",
        ["groq", "ollama", "gemini"],
        help="Choose your preferred AI provider"
    )

    if provider == "groq":
        st.sidebar.info("💡 **Groq Setup:**\n1. Get free API key from groq.com\n2. Add to .env file as GROQ_API_KEY")
    elif provider == "ollama":
        st.sidebar.info("💡 **Ollama Setup:**\n1. Install Ollama locally\n2. Run: `ollama pull llama3.2`\n3. Start: `ollama serve`")
    elif provider == "gemini":
        st.sidebar.info("💡 **Gemini Setup:**\n1. Get free API key from makersuite.google.com\n2. Add to .env file as GEMINI_API_KEY")

    # Template file upload
    st.sidebar.header("Template")
    uploaded_template = st.sidebar.file_uploader(
        "Upload Excel Template (optional)",
        type=['xlsx'],
        help="Upload your test case template. If not provided, the default template will be used."
    )

# Main form
st.header("📝 JIRA Ticket Details")

col1, col2 = st.columns(2)

with col1:
    jira_ticket = st.text_input(
        "JIRA Ticket Number *",
        placeholder="e.g., PROJ-123",
        help="Enter the JIRA ticket identifier"
    )
    
    priority = st.selectbox(
        "Priority *",
        ["High", "Medium", "Low", "Critical", "Blocker"],
        index=1
    )

with col2:
    component = st.text_input(
        "Component",
        value="Web Application",
        help="The component or module being tested"
    )
    
    release = st.text_input(
        "Release Version",
        value="1.0",
        help="Target release version"
    )

test_type = st.selectbox(
    "Test Type",
    ["Functional", "Integration", "API", "UI", "Performance", "Security", "Regression"],
    help="Type of testing to be performed"
)

acceptance_criteria = st.text_area(
    "Acceptance Criteria *",
    height=150,
    placeholder="Enter the acceptance criteria for this ticket...\n\nExample:\n- User should be able to login with valid credentials\n- Error message should display for invalid credentials\n- User should be redirected to dashboard after successful login",
    help="Detailed acceptance criteria that the test cases should validate"
)

# Security warning
if acceptance_criteria:
    if any(sensitive in acceptance_criteria.lower() for sensitive in ['password', 'secret', 'key', 'token', 'credential']):
        st.warning("⚠️ **Security Notice**: Avoid including actual passwords, API keys, or sensitive credentials in acceptance criteria. Use placeholder values like 'valid_password' or '[API_KEY]' instead.")

# Advanced options
with st.expander("⚙️ Advanced Options"):
    col3, col4 = st.columns(2)
    
    with col3:
        test_status = st.selectbox(
            "Test Case Status",
            ["Draft", "Review", "Approved", "Ready"],
            help="Initial status for generated test cases"
        )
    
    with col4:
        automation_status = st.selectbox(
            "Automation Status",
            ["Not Automated", "To Be Automated", "Automated", "Cannot Be Automated"],
            help="Automation readiness status"
        )

# Generate button
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    generate_btn = st.button(
        "🚀 Generate Test Cases",
        type="primary",
        use_container_width=True,
        disabled=not (jira_ticket and priority and acceptance_criteria)
    )

if generate_btn:
    if not jira_ticket or not priority or not acceptance_criteria:
        st.error("Please fill in all required fields (*)")
    else:
        with st.spinner("Generating test cases using AI... This may take a few moments."):
            try:
                # Create test data object
                test_data = TestCaseData(
                    jira_ticket=jira_ticket,
                    priority=priority,
                    acceptance_criteria=acceptance_criteria,
                    component=component,
                    release=release,
                    test_type=test_type
                )
                
                # Initialize generator
                generator = TestCaseGenerator(provider)
                
                # Handle template
                template_path = "Testcases_template.xlsx"
                if uploaded_template:
                    # Save uploaded template to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                        tmp_file.write(uploaded_template.getvalue())
                        template_path = tmp_file.name
                
                # Create testcases directory if it doesn't exist
                testcases_dir = "testcases"
                os.makedirs(testcases_dir, exist_ok=True)
                
                # Generate test cases with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{jira_ticket}_testcases_{timestamp}.xlsx"
                output_path = os.path.join(testcases_dir, output_filename)
                success = generator.generate_from_template(template_path, output_path, test_data)
                
                if success:
                    st.success(f"✅ Test cases generated successfully!")
                    st.info(f"📁 File saved to: `{output_path}`")
                    
                    # Display generated test cases
                    df = pd.read_excel(output_path)
                    
                    # Show summary
                    st.subheader("📊 Summary")
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        st.metric("Total Test Cases", len(df))
                    with col_s2:
                        st.metric("JIRA Ticket", jira_ticket)
                    with col_s3:
                        st.metric("Priority", priority)
                    
                    # Show test cases table
                    st.subheader("📋 Generated Test Cases")
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button
                    with open(output_path, 'rb') as file:
                        st.download_button(
                            label="📥 Download Excel File",
                            data=file.read(),
                            file_name=output_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            type="primary"
                        )
                    
                    # Clean up temporary files
                    if uploaded_template and os.path.exists(template_path):
                        os.unlink(template_path)
                        
                else:
                    st.error("❌ Failed to generate test cases. Please check your configuration and try again.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Instructions
st.markdown("---")
st.subheader("📚 Instructions")

tab1, tab2, tab3 = st.tabs(["🚀 Quick Start", "⚙️ Setup", "💡 Tips"])

with tab1:
    st.markdown("""
    1. **Fill in the required fields** (marked with *)
    2. **Enter detailed acceptance criteria** - the more detailed, the better the test cases
    3. **Select your AI provider** (Groq for cloud, Ollama for local)
    4. **Click Generate** and wait for the AI to create your test cases
    5. **Download the Excel file** with your generated test cases
    """)

with tab2:
    st.markdown("""
    ### Groq Setup (Recommended - Free tier available)
    1. Visit [groq.com](https://groq.com) and create an account
    2. Get your free API key
    3. Add it to your `.env` file: `GROQ_API_KEY=your_key_here`
    
    ### Ollama Setup (Completely free, runs locally)
    1. Install Ollama from [ollama.ai](https://ollama.ai)
    2. Download a model: `ollama pull llama3.2`
    3. Start the service: `ollama serve`
    4. Ollama will run on `http://localhost:11434`
    """)

with tab3:
    st.markdown("""
    ### Writing Better Acceptance Criteria
    - **Be specific**: Include exact expected behaviors
    - **Use scenarios**: "Given... When... Then..." format works well
    - **Include edge cases**: What should happen when things go wrong?
    - **Add data requirements**: Specify input formats, ranges, etc.
    
    ### Example:
    ```
    - Given a user with valid credentials
      When they enter username and password
      Then they should be logged in and redirected to dashboard
    
    - Given a user with invalid credentials  
      When they attempt to login
      Then an error message "Invalid credentials" should be displayed
    ```
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with ❤️ using Streamlit | "
    "Supports Groq and Ollama AI providers"
    "</div>",
    unsafe_allow_html=True
)
