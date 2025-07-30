#!/usr/bin/env python3
"""
Test script to demonstrate all AI providers (Groq, Gemini, Ollama)
"""

import os
import sys
from test_case_generator import TestCaseGenerator, TestCaseData

def test_provider(provider_name):
    """Test a specific AI provider"""
    print(f"\n🧪 Testing {provider_name.upper()} provider...")
    
    try:
        # Create test data
        test_data = TestCaseData(
            jira_ticket=f"TEST-{provider_name.upper()}",
            priority="High", 
            acceptance_criteria="User should be able to perform bulk upload of customer data via CSV file with validation",
            component="Web Application",
            release="1.0",
            test_type="Functional"
        )
        
        # Create generator
        generator = TestCaseGenerator(provider_name)
        
        # Generate test cases
        output_file = f"test_{provider_name}_output.xlsx"
        success = generator.generate_from_template("Testcases_template.xlsx", output_file, test_data)
        
        if success:
            print(f"✅ {provider_name.upper()} test passed! Output: {output_file}")
            return True
        else:
            print(f"❌ {provider_name.upper()} test failed!")
            return False
            
    except Exception as e:
        print(f"❌ {provider_name.upper()} test failed with error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Test Case Generator with all AI providers")
    print("=" * 60)
    
    # Test each provider
    providers = ["groq", "gemini", "ollama"]
    results = {}
    
    for provider in providers:
        results[provider] = test_provider(provider)
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    
    all_passed = True
    for provider, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL" 
        print(f"{provider.upper():10} : {status}")
        if not passed:
            all_passed = False
    
    print(f"\n🎯 Overall Status: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    # Environment info
    print("\n🔧 Environment Information:")
    print(f"- GROQ_API_KEY: {'✅ Set' if os.getenv('GROQ_API_KEY') else '❌ Not set'}")
    print(f"- GEMINI_API_KEY: {'✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Not set'}")
    print(f"- OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
