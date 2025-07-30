#!/usr/bin/env python3
"""
Test Ollama connection and setup
"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        print("🧪 Testing Ollama connection...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            print("✅ Ollama is running and accessible!")
            print(f"📊 Found {len(models)} models:")
            
            if models:
                for model in models:
                    print(f"   - {model['name']} ({model.get('size', 'unknown size')})")
            else:
                print("   ⚠️  No models found. You need to download a model:")
                print("   Run: ollama pull llama3.2")
            
            return True, models
            
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            return False, []
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        print("💡 Try: ollama serve")
        return False, []
        
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False, []

def test_model_generation():
    """Test generating content with Ollama"""
    try:
        print("\n🤖 Testing model generation...")
        
        payload = {
            "model": "llama3.2",  # or whatever model is available
            "prompt": "Generate a simple test case for user login functionality. Respond with just the test title.",
            "stream": False
        }
        
        response = requests.post("http://localhost:11434/api/generate", 
                               json=payload, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('response', '')
            print("✅ Model generation test successful!")
            print(f"📝 Sample response: {content[:100]}...")
            return True
        else:
            print(f"❌ Generation failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False

def main():
    print("🧪 Ollama Connection Tester")
    print("=" * 40)
    
    # Test connection
    is_connected, models = test_ollama_connection()
    
    if not is_connected:
        print("\n🚀 Next steps:")
        print("1. Start Ollama: ollama serve")
        print("2. Download a model: ollama pull llama3.2")
        print("3. Run this test again")
        return
    
    if not models:
        print("\n📥 You need to download a model:")
        print("Run: ollama pull llama3.2")
        print("Then run this test again")
        return
    
    # Test generation
    if test_model_generation():
        print("\n🎉 Ollama is ready for test case generation!")
        print("\n✅ You can now run:")
        print("   streamlit run streamlit_app.py")
        print("   (Select 'ollama' as the AI provider)")
    else:
        print("\n⚠️  Ollama is connected but model generation failed")
        print("Try downloading a different model: ollama pull llama3.2")

if __name__ == "__main__":
    main()
