import os
import pandas as pd
import requests
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import argparse
import sys
import google.generativeai as genai
from history_manager import TestCaseHistory

# Load environment variables
load_dotenv()

@dataclass
class TestCaseData:
    """Data structure for test case information"""
    jira_ticket: str
    priority: str
    acceptance_criteria: str
    component: str = "Web Application"
    release: str = "1.0"
    test_type: str = "Functional"

class AIProvider:
    """Base class for AI providers"""
    
    def generate_test_cases(self, test_data: TestCaseData) -> List[Dict]:
        raise NotImplementedError

class GroqProvider(AIProvider):
    """Groq AI provider (free tier available)"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = os.getenv('DEFAULT_MODEL', 'llama3-8b-8192')
        
    def generate_test_cases(self, test_data: TestCaseData) -> List[Dict]:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        prompt = self._create_prompt(test_data)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert test case generator. Generate comprehensive test cases in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            test_cases = json.loads(content)
            return self._format_test_cases(test_cases, test_data)
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return self._fallback_test_cases(test_data)
    
    def _create_prompt(self, test_data: TestCaseData) -> str:
        return f"""
Generate comprehensive test cases for the following JIRA ticket:

JIRA Ticket: {test_data.jira_ticket}
Priority: {test_data.priority}
Acceptance Criteria: {test_data.acceptance_criteria}

Please generate 3-5 test cases that cover:
1. Happy path scenarios
2. Edge cases
3. Negative test scenarios
4. Boundary conditions

Return the response as a JSON array with the following structure:
[
  {{
    "title": "Test case title",
    "preconditions": "Prerequisites for the test",
    "test_steps": "Step-by-step instructions",
    "data_for_steps": "Test data needed",
    "expected_results": "Expected outcome",
    "tags": "Relevant tags"
  }}
]

Make sure each test case is detailed and actionable.
"""

    def _format_test_cases(self, test_cases: List[Dict], test_data: TestCaseData) -> List[Dict]:
        """Format test cases to match Excel template columns"""
        formatted_cases = []
        
        for i, tc in enumerate(test_cases, 1):
            formatted_case = {
                'Test Key': f"{test_data.jira_ticket}-TC-{i:03d}",
                'Title': tc.get('title', ''),
                'Preconditions': tc.get('preconditions', ''),
                'Priority': test_data.priority,
                'Test Steps': tc.get('test_steps', ''),
                'Data for Steps': tc.get('data_for_steps', ''),
                'Expected Results': tc.get('expected_results', ''),
                'Jira Story ID': test_data.jira_ticket,
                'Test Type': test_data.test_type,
                'Component': test_data.component,
                'Release': test_data.release,
                'Test Case Status': os.getenv('DEFAULT_TEST_STATUS', 'Draft'),
                'Tags': tc.get('tags', ''),
                'Automation Status': os.getenv('DEFAULT_AUTOMATION_STATUS', 'Not Automated'),
                'Automation Key': ''
            }
            formatted_cases.append(formatted_case)
            
        return formatted_cases
    
    def _fallback_test_cases(self, test_data: TestCaseData) -> List[Dict]:
        """Fallback test cases if AI generation fails"""
        return [{
            'Test Key': f"{test_data.jira_ticket}-TC-001",
            'Title': f"Verify {test_data.jira_ticket} acceptance criteria",
            'Preconditions': "Application is accessible and user is logged in",
            'Priority': test_data.priority,
            'Test Steps': "1. Navigate to the feature\n2. Perform the required action\n3. Verify the result",
            'Data for Steps': "Valid test data",
            'Expected Results': "Feature works as per acceptance criteria",
            'Jira Story ID': test_data.jira_ticket,
            'Test Type': test_data.test_type,
            'Component': test_data.component,
            'Release': test_data.release,
            'Test Case Status': 'Draft',
            'Tags': 'smoke, regression',
            'Automation Status': 'Not Automated',
            'Automation Key': ''
        }]

class OllamaProvider(AIProvider):
    """Ollama provider (completely free, local)"""
    
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = "llama3.2"  # or any model you have installed
    
    def generate_test_cases(self, test_data: TestCaseData) -> List[Dict]:
        prompt = self._create_prompt(test_data)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result['response']
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                start = content.find('[')
                end = content.rfind(']') + 1
                if start != -1 and end != 0:
                    json_content = content[start:end]
                    test_cases = json.loads(json_content)
                    return self._format_test_cases(test_cases, test_data)
            except:
                pass
                
            return self._fallback_test_cases(test_data)
            
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            print("Make sure Ollama is running locally with: ollama serve")
            return self._fallback_test_cases(test_data)
    
    def _create_prompt(self, test_data: TestCaseData) -> str:
        return f"""
Generate comprehensive test cases for the following JIRA ticket:

JIRA Ticket: {test_data.jira_ticket}
Priority: {test_data.priority}
Acceptance Criteria: {test_data.acceptance_criteria}

Please generate 3-5 test cases that cover:
1. Happy path scenarios
2. Edge cases
3. Negative test scenarios
4. Boundary conditions

Return the response as a JSON array with the following structure:
[
  {{
    "title": "Test case title",
    "preconditions": "Prerequisites for the test",
    "test_steps": "Step-by-step instructions",
    "data_for_steps": "Test data needed",
    "expected_results": "Expected outcome",
    "tags": "Relevant tags"
  }}
]

Make sure each test case is detailed and actionable.
"""

    def _format_test_cases(self, test_cases: List[Dict], test_data: TestCaseData) -> List[Dict]:
        """Format test cases to match Excel template columns"""
        formatted_cases = []
        
        for i, tc in enumerate(test_cases, 1):
            formatted_case = {
                'Test Key': f"{test_data.jira_ticket}-TC-{i:03d}",
                'Title': tc.get('title', ''),
                'Preconditions': tc.get('preconditions', ''),
                'Priority': test_data.priority,
                'Test Steps': tc.get('test_steps', ''),
                'Data for Steps': tc.get('data_for_steps', ''),
                'Expected Results': tc.get('expected_results', ''),
                'Jira Story ID': test_data.jira_ticket,
                'Test Type': test_data.test_type,
                'Component': test_data.component,
                'Release': test_data.release,
                'Test Case Status': os.getenv('DEFAULT_TEST_STATUS', 'Draft'),
                'Tags': tc.get('tags', ''),
                'Automation Status': os.getenv('DEFAULT_AUTOMATION_STATUS', 'Not Automated'),
                'Automation Key': ''
            }
            formatted_cases.append(formatted_case)
            
        return formatted_cases
    
    def _fallback_test_cases(self, test_data: TestCaseData) -> List[Dict]:
        """Fallback test cases if AI generation fails"""
        return [{
            'Test Key': f"{test_data.jira_ticket}-TC-001",
            'Title': f"Verify {test_data.jira_ticket} acceptance criteria",
            'Preconditions': "Application is accessible and user is logged in",
            'Priority': test_data.priority,
            'Test Steps': "1. Navigate to the feature\n2. Perform the required action\n3. Verify the result",
            'Data for Steps': "Valid test data",
            'Expected Results': "Feature works as per acceptance criteria",
            'Jira Story ID': test_data.jira_ticket,
            'Test Type': test_data.test_type,
            'Component': test_data.component,
            'Release': test_data.release,
            'Test Case Status': 'Draft',
            'Tags': 'smoke, regression',
            'Automation Status': 'Not Automated',
            'Automation Key': ''
        }]

class GeminiProvider(AIProvider):
    """Google Gemini AI provider"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate_test_cases(self, test_data: TestCaseData) -> List[Dict]:
        prompt = self._create_prompt(test_data)
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                start = content.find('[')
                end = content.rfind(']') + 1
                if start != -1 and end != 0:
                    json_content = content[start:end]
                    test_cases = json.loads(json_content)
                    return self._format_test_cases(test_cases, test_data)
            except Exception as parse_error:
                print(f"Error parsing JSON from Gemini response: {parse_error}")
                print(f"Raw response: {content[:500]}...")
                
            return self._fallback_test_cases(test_data)
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._fallback_test_cases(test_data)
    
    def _create_prompt(self, test_data: TestCaseData) -> str:
        return f"""
Generate comprehensive test cases for the following JIRA ticket:

JIRA Ticket: {test_data.jira_ticket}
Priority: {test_data.priority}
Acceptance Criteria: {test_data.acceptance_criteria}

Please generate 3-5 test cases that cover:
1. Happy path scenarios
2. Edge cases
3. Negative test scenarios
4. Boundary conditions

Return the response as a JSON array with the following structure:
[
  {{
    "title": "Test case title",
    "preconditions": "Prerequisites for the test",
    "test_steps": "Step-by-step instructions",
    "data_for_steps": "Test data needed",
    "expected_results": "Expected outcome",
    "tags": "Relevant tags"
  }}
]

Make sure each test case is detailed and actionable. Return ONLY the JSON array, no additional text or formatting.
"""

    def _format_test_cases(self, test_cases: List[Dict], test_data: TestCaseData) -> List[Dict]:
        """Format test cases to match Excel template columns"""
        formatted_cases = []
        
        for i, tc in enumerate(test_cases, 1):
            formatted_case = {
                'Test Key': f"{test_data.jira_ticket}-TC-{i:03d}",
                'Title': tc.get('title', ''),
                'Preconditions': tc.get('preconditions', ''),
                'Priority': test_data.priority,
                'Test Steps': tc.get('test_steps', ''),
                'Data for Steps': tc.get('data_for_steps', ''),
                'Expected Results': tc.get('expected_results', ''),
                'Jira Story ID': test_data.jira_ticket,
                'Test Type': test_data.test_type,
                'Component': test_data.component,
                'Release': test_data.release,
                'Test Case Status': os.getenv('DEFAULT_TEST_STATUS', 'Draft'),
                'Tags': tc.get('tags', ''),
                'Automation Status': os.getenv('DEFAULT_AUTOMATION_STATUS', 'Not Automated'),
                'Automation Key': ''
            }
            formatted_cases.append(formatted_case)
            
        return formatted_cases
    
    def _fallback_test_cases(self, test_data: TestCaseData) -> List[Dict]:
        """Fallback test cases if AI generation fails"""
        return [{
            'Test Key': f"{test_data.jira_ticket}-TC-001",
            'Title': f"Verify {test_data.jira_ticket} acceptance criteria",
            'Preconditions': "Application is accessible and user is logged in",
            'Priority': test_data.priority,
            'Test Steps': "1. Navigate to the feature\n2. Perform the required action\n3. Verify the result",
            'Data for Steps': "Valid test data",
            'Expected Results': "Feature works as per acceptance criteria",
            'Jira Story ID': test_data.jira_ticket,
            'Test Type': test_data.test_type,
            'Component': test_data.component,
            'Release': test_data.release,
            'Test Case Status': 'Draft',
            'Tags': 'smoke, regression',
            'Automation Status': 'Not Automated',
            'Automation Key': ''
        }]

class TestCaseGenerator:
    """Main test case generator class"""
    
    def __init__(self, provider: str = "groq"):
        self.provider = self._get_provider(provider)
    
    def _get_provider(self, provider_name: str) -> AIProvider:
        """Get AI provider based on name"""
        if provider_name.lower() == "groq":
            return GroqProvider()
        elif provider_name.lower() == "ollama":
            return OllamaProvider()
        elif provider_name.lower() == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
    
    def generate_from_template(self, template_path: str, output_path: str, test_data: TestCaseData, record_history: bool = True) -> bool:
        """Generate test cases and save to Excel file"""
        try:
            # Read existing template
            if os.path.exists(template_path):
                df_template = pd.read_excel(template_path)
                print(f"Loaded template with {len(df_template)} existing rows")
            else:
                # Create new dataframe with template columns
                columns = [
                    'Test Key', 'Title', 'Preconditions', 'Priority', 'Test Steps',
                    'Data for Steps', 'Expected Results', 'Jira Story ID', 'Test Type',
                    'Component', 'Release', 'Test Case Status', 'Tags',
                    'Automation Status', 'Automation Key'
                ]
                df_template = pd.DataFrame(columns=columns)
                print("Created new template structure")
            
            # Generate test cases using AI
            print("Generating test cases using AI...")
            test_cases = self.provider.generate_test_cases(test_data)
            
            if not test_cases:
                print("No test cases generated")
                return False
            
            # Convert to DataFrame
            df_new_cases = pd.DataFrame(test_cases)
            
            # Append to existing template
            df_combined = pd.concat([df_template, df_new_cases], ignore_index=True)
            
            # Save to Excel
            df_combined.to_excel(output_path, index=False)
            print(f"Generated {len(test_cases)} test cases and saved to {output_path}")
            
            # Record in history if requested
            if record_history:
                try:
                    history = TestCaseHistory()
                    provider_name = self.provider.__class__.__name__.replace('Provider', '').lower()
                    history.add_entry(
                        jira_ticket=test_data.jira_ticket,
                        priority=test_data.priority,
                        acceptance_criteria=test_data.acceptance_criteria,
                        file_path=output_path,
                        provider=provider_name,
                        component=test_data.component,
                        test_type=test_data.test_type
                    )
                    print(f"📝 Recorded in history: {output_path}")
                except Exception as e:
                    print(f"⚠️ Warning: Could not record history: {e}")
            
            return True
            
        except Exception as e:
            print(f"Error generating test cases: {e}")
            return False

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Generate test cases from JIRA ticket details")
    parser.add_argument("--jira", required=True, help="JIRA ticket number")
    parser.add_argument("--priority", required=True, help="Priority (High, Medium, Low)")
    parser.add_argument("--criteria", required=True, help="Acceptance criteria")
    parser.add_argument("--provider", default="groq", help="AI provider (groq, ollama, gemini)")
    parser.add_argument("--template", default="Testcases_template.xlsx", help="Template file path")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--component", default="Web Application", help="Component name")
    parser.add_argument("--release", default="1.0", help="Release version")
    parser.add_argument("--test-type", default="Functional", help="Test type")
    
    args = parser.parse_args()
    
    # Set output file name if not provided
    if not args.output:
        # Create testcases directory if it doesn't exist
        testcases_dir = "testcases"
        os.makedirs(testcases_dir, exist_ok=True)
        args.output = os.path.join(testcases_dir, f"{args.jira}_testcases.xlsx")
    
    # Create test data object
    test_data = TestCaseData(
        jira_ticket=args.jira,
        priority=args.priority,
        acceptance_criteria=args.criteria,
        component=args.component,
        release=args.release,
        test_type=args.test_type
    )
    
    # Generate test cases
    generator = TestCaseGenerator(args.provider)
    success = generator.generate_from_template(args.template, args.output, test_data)
    
    if success:
        print(f"\n✅ Test cases successfully generated!")
        print(f"📁 Output file: {args.output}")
    else:
        print("\n❌ Failed to generate test cases")
        sys.exit(1)

if __name__ == "__main__":
    main()
