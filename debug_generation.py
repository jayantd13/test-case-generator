#!/usr/bin/env python3
"""
Simple test to debug the bulk upload test case generation issue
"""

import os
import sys

def test_basic_functionality():
    """Test basic functionality step by step"""
    
    print("🔍 Debugging Test Case Generation Issue")
    print("=" * 50)
    
    # Test 1: Check if required modules can be imported
    print("1. Testing imports...")
    try:
        import pandas as pd
        import requests
        from test_case_generator import TestCaseGenerator, TestCaseData
        print("   ✅ All imports successful")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # Test 2: Check environment variables
    print("\n2. Checking environment...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        provider = os.getenv('DEFAULT_AI_PROVIDER', 'ollama')
        print(f"   ✅ Default provider: {provider}")
        
        if provider == 'ollama':
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            print(f"   ✅ Ollama URL: {ollama_url}")
        
    except Exception as e:
        print(f"   ❌ Environment error: {e}")
    
    # Test 3: Check Ollama connection
    print("\n3. Testing Ollama connection...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"   ✅ Ollama connected, {len(models)} models available")
            for model in models:
                print(f"      - {model['name']}")
        else:
            print(f"   ❌ Ollama responded with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ollama connection error: {e}")
        print("   💡 Make sure Ollama is running: ollama serve")
    
    # Test 4: Create test data
    print("\n4. Creating test data...")
    try:
        test_data = TestCaseData(
            jira_ticket="DEBUG-001",
            priority="High",
            acceptance_criteria="Simple test: User should be able to login with valid credentials.",
            component="Test",
            release="1.0",
            test_type="Functional"
        )
        print("   ✅ Test data created successfully")
        print(f"   📋 JIRA: {test_data.jira_ticket}")
        print(f"   📋 Criteria: {test_data.acceptance_criteria[:50]}...")
        
    except Exception as e:
        print(f"   ❌ Test data creation error: {e}")
        return False
    
    # Test 5: Try to initialize generator
    print("\n5. Testing generator initialization...")
    try:
        generator = TestCaseGenerator("ollama")
        print("   ✅ Generator initialized with Ollama")
    except Exception as e:
        print(f"   ❌ Generator initialization error: {e}")
        try:
            # Try fallback without provider
            print("   🔄 Trying fallback...")
            # We'll create a simple manual test case instead
            manual_test_case = create_manual_test_case(test_data)
            print("   ✅ Manual fallback successful")
            return True
        except Exception as e2:
            print(f"   ❌ Fallback also failed: {e2}")
            return False
    
    # Test 6: Generate a simple test case
    print("\n6. Testing test case generation...")
    try:
        success = generator.generate_from_template(
            "Testcases_template.xlsx", 
            "DEBUG-001_test.xlsx", 
            test_data
        )
        
        if success:
            print("   ✅ Test case generation successful!")
            
            # Check the output
            import pandas as pd
            df = pd.read_excel("DEBUG-001_test.xlsx")
            print(f"   📊 Generated {len(df)} test cases")
            
            if len(df) > 0:
                print(f"   📝 First test case: {df.iloc[0]['Title']}")
            
        else:
            print("   ❌ Test case generation failed")
            
    except Exception as e:
        print(f"   ❌ Generation error: {e}")
        print(f"   🔍 Full error: {str(e)}")
        
        # Try manual generation as fallback
        print("\n   🔄 Trying manual generation...")
        try:
            manual_test_case = create_manual_test_case(test_data)
            save_manual_test_case(manual_test_case, "DEBUG-001_manual.xlsx")
            print("   ✅ Manual generation successful!")
        except Exception as e2:
            print(f"   ❌ Manual generation also failed: {e2}")

def create_manual_test_case(test_data):
    """Create a manual test case as fallback"""
    return {
        'Test Key': f"{test_data.jira_ticket}-TC-001",
        'Title': f"Verify {test_data.acceptance_criteria.split('.')[0]}",
        'Preconditions': "System is accessible and user has valid credentials",
        'Priority': test_data.priority,
        'Test Steps': "1. Navigate to login page\n2. Enter valid credentials\n3. Click login button\n4. Verify successful login",
        'Data for Steps': "Valid username and password",
        'Expected Results': "User is successfully logged in and redirected to dashboard",
        'Jira Story ID': test_data.jira_ticket,
        'Test Type': test_data.test_type,
        'Component': test_data.component,
        'Release': test_data.release,
        'Test Case Status': 'Draft',
        'Tags': 'login, authentication',
        'Automation Status': 'Not Automated',
        'Automation Key': ''
    }

def save_manual_test_case(test_case, filename):
    """Save manual test case to Excel"""
    import pandas as pd
    df = pd.DataFrame([test_case])
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    test_basic_functionality()
    
    print("\n" + "=" * 50)
    print("🎯 Summary and Recommendations")
    print("=" * 50)
    
    print("\nFor your bulk upload requirements, here's what I recommend:")
    print("\n1. 📝 Break down acceptance criteria into smaller sections:")
    print("   - Navigation and access")
    print("   - File upload functionality") 
    print("   - Data processing and validation")
    print("   - UI display requirements")
    print("   - Download functionality")
    
    print("\n2. 🔧 If AI generation fails, use manual test cases:")
    print("   - More reliable for complex requirements")
    print("   - Better control over test case quality")
    print("   - Can include specific business logic")
    
    print("\n3. 🤖 AI Provider troubleshooting:")
    print("   - Ollama: Make sure 'ollama serve' is running")
    print("   - Groq: Check API key in .env file")
    print("   - Try shorter, more focused acceptance criteria")
    
    print("\n4. 💡 For your specific bulk upload feature:")
    print("   - Test file upload process separately")
    print("   - Test data validation separately") 
    print("   - Test UI display separately")
    print("   - Test download functionality separately")
    
    print(f"\n📁 Check generated files in: {os.getcwd()}")
    print("🎉 Debug complete!")
