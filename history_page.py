import streamlit as st
import pandas as pd
import os
from datetime import datetime
from history_manager import TestCaseHistory

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

if __name__ == "__main__":
    show_history_page()
