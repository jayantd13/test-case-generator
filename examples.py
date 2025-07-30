#!/usr/bin/env python3
"""
Example usage of the Test Case Generator
"""

from test_case_generator import TestCaseGenerator, TestCaseData

def example_login_feature():
    """Example: Generate test cases for a login feature"""
    
    print("🧪 Example: Login Feature Test Cases")
    print("=" * 50)
    
    # Define test data
    test_data = TestCaseData(
        jira_ticket="AUTH-101",
        priority="High",
        acceptance_criteria="""
        User Login Functionality:
        - User should be able to login with valid email and password
        - Valid credentials should redirect user to dashboard
        - Invalid credentials should display error message "Invalid email or password"
        - Empty email field should show validation error "Email is required"
        - Empty password field should show validation error "Password is required"
        - Forgot password link should be visible and functional
        - Remember me checkbox should keep user logged in for 30 days
        - After 3 failed attempts, account should be temporarily locked for 15 minutes
        """,
        component="Authentication",
        release="2.0",
        test_type="Functional"
    )
    
    # Initialize generator (try Groq first, fallback to Ollama)
    try:
        generator = TestCaseGenerator("groq")
        print("🚀 Using Groq AI provider")
    except:
        try:
            generator = TestCaseGenerator("ollama")
            print("🚀 Using Ollama AI provider")
        except:
            print("❌ No AI provider available. Please set up Groq or Ollama.")
            return
    
    # Generate test cases
    output_file = f"{test_data.jira_ticket}_example_testcases.xlsx"
    success = generator.generate_from_template(
        "Testcases_template.xlsx", 
        output_file, 
        test_data
    )
    
    if success:
        print(f"✅ Generated test cases saved to: {output_file}")
    else:
        print("❌ Failed to generate test cases")

def example_api_feature():
    """Example: Generate test cases for an API feature"""
    
    print("\n🧪 Example: API Feature Test Cases")
    print("=" * 50)
    
    test_data = TestCaseData(
        jira_ticket="API-205",
        priority="Medium",
        acceptance_criteria="""
        User Profile API:
        - GET /api/users/{id} should return user profile data when valid token provided
        - Response should include: id, name, email, created_date, last_login
        - Should return 401 Unauthorized for invalid or missing token
        - Should return 404 Not Found for non-existent user ID
        - Should return 403 Forbidden when user tries to access another user's profile
        - Response time should be under 200ms for 95% of requests
        - API should handle concurrent requests properly
        - Should return proper error messages in JSON format
        """,
        component="User API",
        release="1.5",
        test_type="API"
    )
    
    try:
        generator = TestCaseGenerator("groq")
        print("🚀 Using Groq AI provider")
    except:
        try:
            generator = TestCaseGenerator("ollama")
            print("🚀 Using Ollama AI provider")
        except:
            print("❌ No AI provider available. Please set up Groq or Ollama.")
            return
    
    output_file = f"{test_data.jira_ticket}_example_testcases.xlsx"
    success = generator.generate_from_template(
        "Testcases_template.xlsx", 
        output_file, 
        test_data
    )
    
    if success:
        print(f"✅ Generated test cases saved to: {output_file}")
    else:
        print("❌ Failed to generate test cases")

if __name__ == "__main__":
    print("🧪 Test Case Generator - Examples")
    print("=" * 40)
    print("This script demonstrates how to use the test case generator")
    print("with different types of features.\n")
    
    # Run examples
    example_login_feature()
    example_api_feature()
    
    print("\n🎉 Examples completed!")
    print("Check the generated Excel files to see the results.")
    print("\nNext steps:")
    print("1. Edit the .env file with your AI provider API key")
    print("2. Run: streamlit run streamlit_app.py (for web interface)")
    print("3. Or use: python test_case_generator.py --help (for CLI)")
