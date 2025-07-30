#!/usr/bin/env python3
"""
Test the bulk upload feature with specific acceptance criteria
"""

from test_case_generator import TestCaseGenerator, TestCaseData

def test_bulk_upload_feature():
    """Test case generation for bulk upload leads functionality"""
    
    print("🧪 Testing Bulk Upload Leads Feature")
    print("=" * 50)
    
    # Define test data with your specific acceptance criteria
    test_data = TestCaseData(
        jira_ticket="BULK-001",
        priority="High",
        acceptance_criteria="""
        Bulk Upload Leads Functionality:
        
        Core Requirements:
        - Bulk Upload leads page should show list of files uploaded
        - Bulk upload leads should generate leads when spreadsheet is uploaded
        - User should be able to download uploaded spreadsheet by clicking on file name
        - Column names in the bulk upload lead spreadsheet should be case insensitive, meaning leads should be created despite column name case
        
        List Page Columns Required:
        - Bulk upload file name
        - Bulk upload identifier  
        - Success count
        - Failed count
        - Error
        - Created date in EST
        - Created by
        
        Navigation Steps:
        1. Login to Marketplace admin
        2. Navigate to Forms
        3. Click on Bulk upload leads
        4. Upload spreadsheet
        
        Additional Requirements:
        - Steps should have serial numbers for each action
        - File upload should process and show results
        - Error handling for invalid files
        - Case insensitive column validation
        - Download functionality for uploaded files
        """,
        component="Bulk Upload",
        release="2.0",
        test_type="Functional"
    )
    
    # Try different AI providers
    providers = ["ollama", "groq"]
    
    for provider in providers:
        try:
            print(f"\n🤖 Trying {provider.upper()} AI provider...")
            generator = TestCaseGenerator(provider)
            
            # Generate test cases
            output_file = f"{test_data.jira_ticket}_bulk_upload_testcases_{provider}.xlsx"
            success = generator.generate_from_template(
                "Testcases_template.xlsx", 
                output_file, 
                test_data
            )
            
            if success:
                print(f"✅ Generated test cases saved to: {output_file}")
                
                # Show generated content summary
                import pandas as pd
                try:
                    df = pd.read_excel(output_file)
                    print(f"📊 Generated {len(df)} test cases:")
                    for idx, row in df.iterrows():
                        print(f"   {idx+1}. {row['Title']}")
                    break  # Success, no need to try other providers
                except Exception as e:
                    print(f"⚠️ Could not read generated file: {e}")
                    
            else:
                print(f"❌ Failed to generate test cases with {provider}")
                
        except Exception as e:
            print(f"❌ Error with {provider}: {e}")
            continue
    
    else:
        print("❌ All AI providers failed. Please check your configuration.")
        print("\n🔧 Troubleshooting:")
        print("1. For Ollama: Make sure it's running (ollama serve)")
        print("2. For Groq: Check your API key in .env file")
        print("3. Check internet connection")

def test_with_improved_prompt():
    """Test with manually crafted test cases as fallback"""
    
    print("\n🧪 Manual Test Case Generation (Fallback)")
    print("=" * 50)
    
    # Create manual test cases as an example
    manual_test_cases = [
        {
            'Test Key': 'BULK-001-TC-001',
            'Title': 'Verify bulk upload leads page displays list of uploaded files',
            'Preconditions': 'User is logged into Marketplace admin with proper permissions',
            'Priority': 'High',
            'Test Steps': '''1. Login to Marketplace admin with valid credentials
2. Navigate to Forms section from main menu
3. Click on "Bulk upload leads" option
4. Verify the bulk upload leads page loads successfully
5. Check if previously uploaded files are displayed in the list''',
            'Data for Steps': 'Valid admin credentials, existing uploaded files (if any)',
            'Expected Results': '''- Bulk upload leads page loads without errors
- List of uploaded files is displayed with all required columns:
  * Bulk upload file name
  * Bulk upload identifier
  * Success count
  * Failed count  
  * Error status
  * Created date in EST timezone
  * Created by user''',
            'Jira Story ID': 'BULK-001',
            'Test Type': 'Functional',
            'Component': 'Bulk Upload',
            'Release': '2.0',
            'Test Case Status': 'Draft',
            'Tags': 'bulk-upload, ui-validation, file-list',
            'Automation Status': 'Not Automated',
            'Automation Key': ''
        },
        {
            'Test Key': 'BULK-001-TC-002',
            'Title': 'Verify successful lead generation from uploaded spreadsheet',
            'Preconditions': 'User is on bulk upload leads page with valid spreadsheet file',
            'Priority': 'High',
            'Test Steps': '''1. Login to Marketplace admin
2. Navigate to Forms > Bulk upload leads
3. Click on upload button/area
4. Select a valid Excel/CSV file with lead data
5. Click upload to submit the file
6. Wait for processing to complete
7. Verify leads are created successfully
8. Check success count is updated correctly''',
            'Data for Steps': 'Valid spreadsheet with proper column headers (Name, Email, Phone, etc.)',
            'Expected Results': '''- File uploads successfully without errors
- Processing indicator shows while file is being processed
- Leads are created in the system
- Success count reflects number of leads created
- Failed count shows any records that failed processing
- Upload entry appears in the list with correct statistics''',
            'Jira Story ID': 'BULK-001',
            'Test Type': 'Functional',
            'Component': 'Bulk Upload',
            'Release': '2.0',
            'Test Case Status': 'Draft',
            'Tags': 'bulk-upload, lead-generation, file-processing',
            'Automation Status': 'Not Automated',
            'Automation Key': ''
        },
        {
            'Test Key': 'BULK-001-TC-003',
            'Title': 'Verify case insensitive column name handling in spreadsheet',
            'Preconditions': 'User has spreadsheet with mixed case column headers',
            'Priority': 'Medium',
            'Test Steps': '''1. Login to Marketplace admin
2. Navigate to Forms > Bulk upload leads
3. Prepare test spreadsheet with mixed case headers (e.g., "NAME", "email", "Phone")
4. Upload the spreadsheet file
5. Wait for processing to complete
6. Verify leads are created despite mixed case column names
7. Check that all data is correctly mapped''',
            'Data for Steps': 'Spreadsheet with headers like: NAME, email, Phone, COMPANY, address',
            'Expected Results': '''- System accepts mixed case column headers
- Leads are created successfully
- Data is correctly mapped to appropriate fields
- No errors related to column case sensitivity
- Success count reflects all valid records processed''',
            'Jira Story ID': 'BULK-001',
            'Test Type': 'Functional',
            'Component': 'Bulk Upload',
            'Release': '2.0',
            'Test Case Status': 'Draft',
            'Tags': 'bulk-upload, case-insensitive, data-validation',
            'Automation Status': 'Not Automated',
            'Automation Key': ''
        },
        {
            'Test Key': 'BULK-001-TC-004',
            'Title': 'Verify download functionality for uploaded spreadsheet files',
            'Preconditions': 'Files have been previously uploaded to the system',
            'Priority': 'Medium',
            'Test Steps': '''1. Login to Marketplace admin
2. Navigate to Forms > Bulk upload leads
3. Locate an uploaded file in the list
4. Click on the file name link
5. Verify download begins automatically
6. Check downloaded file content matches original upload
7. Verify file format is preserved''',
            'Data for Steps': 'Previously uploaded Excel/CSV files in the system',
            'Expected Results': '''- Clicking file name initiates download
- File downloads successfully to default download location
- Downloaded file contains original data
- File format and structure are preserved
- No corruption or data loss in downloaded file''',
            'Jira Story ID': 'BULK-001',
            'Test Type': 'Functional',
            'Component': 'Bulk Upload',
            'Release': '2.0',
            'Test Case Status': 'Draft',
            'Tags': 'bulk-upload, file-download, data-integrity',
            'Automation Status': 'Not Automated',
            'Automation Key': ''
        }
    ]
    
    # Save manual test cases to Excel
    import pandas as pd
    
    df = pd.DataFrame(manual_test_cases)
    output_file = "BULK-001_manual_testcases.xlsx"
    df.to_excel(output_file, index=False)
    
    print(f"✅ Manual test cases saved to: {output_file}")
    print(f"📊 Generated {len(manual_test_cases)} comprehensive test cases")
    
    print("\n📋 Test Cases Created:")
    for i, tc in enumerate(manual_test_cases, 1):
        print(f"   {i}. {tc['Title']}")

if __name__ == "__main__":
    print("🧪 Bulk Upload Test Case Generator")
    print("=" * 40)
    print("Testing AI generation with your specific acceptance criteria...")
    
    # Try AI generation first
    test_bulk_upload_feature()
    
    # Generate manual test cases as reference
    test_with_improved_prompt()
    
    print("\n🎉 Test case generation completed!")
    print("\n💡 Tips for better AI generation:")
    print("1. Break down complex requirements into smaller sections")
    print("2. Use clear 'Given-When-Then' format")
    print("3. Specify exact expected outcomes")
    print("4. Include specific test data requirements")
    print("5. Make navigation steps very explicit")
