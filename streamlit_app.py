import streamlit as st
import pandas as pd
import os
from test_case_generator import TestCaseGenerator, TestCaseData
from history_manager import TestCaseHistory
import tempfile
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Test Case Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def format_datetime(iso_string):
    """Format ISO datetime string to readable format"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return iso_string

def show_generator_page():
    """Show the main test case generation page"""
    
    st.title("🧪 Test Case Generator")
    st.markdown("Generate comprehensive test cases from JIRA ticket details using AI")

    # AI Provider selection
    provider = st.selectbox(
        "Select AI Provider",
        ["groq", "ollama", "gemini"],
        help="Choose your preferred AI provider"
    )

    if provider == "groq":
        st.info("💡 **Groq Setup:** Get free API key from groq.com and add to .env file as GROQ_API_KEY")
    elif provider == "ollama":
        st.info("💡 **Ollama Setup:** Install Ollama locally, run `ollama pull llama3.2` and start with `ollama serve`")
    elif provider == "gemini":
        st.info("💡 **Gemini Setup:** Get free API key from makersuite.google.com and add to .env file as GEMINI_API_KEY")

    # Template file upload
    st.subheader("📄 Template (Optional)")
    uploaded_template = st.file_uploader(
        "Upload Excel Template",
        type=['xlsx'],
        help="Upload your test case template. If not provided, the default template will be used."
    )

    # Main form
    st.subheader("📝 JIRA Ticket Details")

    col1, col2 = st.columns(2)

    with col1:
        jira_ticket = st.text_input(
            "JIRA Ticket Number *",
            placeholder="e.g., PROJ-123",
            help="Enter the JIRA ticket identifier"
        )
        
        priority = st.selectbox(
            "Priority *",
            ["High", "Medium", "Low"],
            help="Select the test priority level"
        )

    with col2:
        component = st.text_input(
            "Component",
            value="Web Application",
            help="Component or module being tested"
        )
        
        release = st.text_input(
            "Release Version",
            value="1.0",
            help="Target release version"
        )

    # Acceptance criteria
    acceptance_criteria = st.text_area(
        "Acceptance Criteria *",
        placeholder="Describe the feature requirements and expected behavior...",
        height=150,
        help="Detailed acceptance criteria for the feature"
    )

    # Additional options
    col3, col4 = st.columns(2)

    with col3:
        test_type = st.selectbox(
            "Test Type",
            ["Functional", "API", "UI", "Integration", "Regression", "Performance"],
            help="Type of testing to be performed"
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

def show_history_page():
    """Display the test case generation history page"""
    
    st.title("📜 Test Case Generation History")
    st.markdown("View and manage all previously generated test cases")
    
    # Initialize history manager
    history = TestCaseHistory()
    
    # Get all entries
    entries = history.get_all_entries()
    stats = history.get_stats()
    
    # Show statistics
    st.subheader("📊 Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Generations", stats["total_entries"])
    
    with col2:
        st.metric("Available Files", stats["total_files"])
    
    with col3:
        if stats["total_size"] > 0:
            st.metric("Total Size", format_file_size(stats["total_size"]))
        else:
            st.metric("Total Size", "0 B")
    
    with col4:
        if stats["providers_used"]:
            st.metric("Providers Used", len(stats["providers_used"]))
        else:
            st.metric("Providers Used", "0")
    
    if not entries:
        st.info("📝 No test case generation history found. Start generating test cases to see them here!")
        return
    
    # Search and filter options
    st.subheader("🔍 Search & Filter")
    col_search1, col_search2 = st.columns(2)
    
    with col_search1:
        search_term = st.text_input("Search by JIRA ticket or criteria", placeholder="e.g., BULK-001")
    
    with col_search2:
        provider_filter = st.selectbox(
            "Filter by Provider",
            ["All"] + stats["providers_used"]
        )
    
    # Filter entries
    filtered_entries = entries
    
    if search_term:
        filtered_entries = [
            entry for entry in filtered_entries
            if search_term.lower() in entry.get('jira_ticket', '').lower() or
               search_term.lower() in entry.get('acceptance_criteria', '').lower()
        ]
    
    if provider_filter != "All":
        filtered_entries = [
            entry for entry in filtered_entries
            if entry.get('provider', '').lower() == provider_filter.lower()
        ]
    
    st.subheader(f"📋 History ({len(filtered_entries)} entries)")
    
    # Display entries
    for idx, entry in enumerate(filtered_entries):
        with st.expander(f"🎫 {entry.get('jira_ticket', 'Unknown')} - {entry.get('priority', 'Medium')} Priority", expanded=False):
            
            # Entry details
            col_detail1, col_detail2 = st.columns([2, 1])
            
            with col_detail1:
                st.markdown(f"**JIRA Ticket:** {entry.get('jira_ticket', 'N/A')}")
                st.markdown(f"**Priority:** {entry.get('priority', 'N/A')}")
                st.markdown(f"**Component:** {entry.get('component', 'N/A')}")
                st.markdown(f"**Test Type:** {entry.get('test_type', 'N/A')}")
                st.markdown(f"**Provider:** {entry.get('provider', 'N/A').title()}")
                
                # Acceptance Criteria
                st.markdown("**Acceptance Criteria:**")
                criteria_text = entry.get('acceptance_criteria', 'No criteria provided')
                if len(criteria_text) > 200:
                    with st.expander("View Full Acceptance Criteria"):
                        st.text_area("", criteria_text, height=100, disabled=True, key=f"criteria_{idx}")
                    st.markdown(f"{criteria_text[:200]}...")
                else:
                    st.markdown(criteria_text)
            
            with col_detail2:
                st.markdown(f"**Created:** {format_datetime(entry.get('created_date', ''))}")
                st.markdown(f"**File Size:** {format_file_size(entry.get('file_size', 0))}")
                
                # File download
                file_path = entry.get('file_path', '')
                file_name = entry.get('file_name', 'file.xlsx')
                
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        st.download_button(
                            label=f"📥 Download {file_name}",
                            data=file.read(),
                            file_name=file_name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_{idx}"
                        )
                else:
                    st.error("❌ File not found")
                
                # Delete button
                if st.button("🗑️ Delete Entry", key=f"delete_{idx}", help="Delete this history entry"):
                    if history.delete_entry(entry.get('id')):
                        st.success("Entry deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete entry")

def show_about_page():
    """Show the about page"""
    st.title("ℹ️ About Test Case Generator")
    
    st.markdown("""
    ## 🎯 Purpose
    This tool helps QA teams and developers automatically generate comprehensive test cases from JIRA ticket details using AI.
    
    ## 🚀 Features
    - **AI-Powered Generation**: Uses Groq, Gemini, or Ollama for intelligent test case creation
    - **Excel Integration**: Works with your existing Excel templates
    - **History Tracking**: Keep track of all generated test cases
    - **Multiple Providers**: Choose from different AI providers
    - **Web Interface**: Easy-to-use interface for non-technical users
    
    ## 📊 Supported AI Providers
    - **Groq**: Fast and reliable cloud-based AI (free tier)
    - **Google Gemini**: Google's powerful AI model (free tier)
    - **Ollama**: Local AI that runs on your machine (completely free)
    
    ## 🛠️ Technical Details
    - Built with Streamlit and Python
    - Supports Excel (.xlsx) file format
    - Automatic file organization in `testcases/` folder
    - History stored in JSON format
    
    ## 📝 Usage Tips
    1. Fill in detailed acceptance criteria for better test cases
    2. Use specific JIRA ticket numbers for easy tracking
    3. Review generated test cases before using them
    4. Download and customize test cases as needed
    
    ## 🔗 Navigation
    - **Generate Test Cases**: Create new test cases from JIRA tickets
    - **History**: View and download previously generated test cases
    - **About**: This information page
    """)

# Navigation
st.sidebar.title("🧪 Test Case Generator")
page = st.sidebar.radio(
    "Navigate to:",
    ["🚀 Generate Test Cases", "📜 History", "ℹ️ About"],
    index=0
)

# Route to appropriate page
if page == "🚀 Generate Test Cases":
    show_generator_page()
elif page == "📜 History":
    show_history_page()
elif page == "ℹ️ About":
    show_about_page()
