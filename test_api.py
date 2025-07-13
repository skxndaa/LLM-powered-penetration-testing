#!/usr/bin/env python3
"""
Quick test to verify Groq API connection
"""

import sys
import os
from groq import Groq
from config import Config

def test_groq_api():
    """Test the Groq API connection"""
    print("🔑 Testing Groq API Connection")
    print("=" * 40)
    
    # Load API key
    api_key = Config.get_groq_api_key()
    if not api_key:
        print("❌ No API key found!")
        print("Run: python3 setup_api_key.py")
        return False
    
    print(f"✅ API key loaded: {api_key[:8]}..." + "*" * (len(api_key) - 8))
    
    try:
        # Initialize client
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized")
        
        # Test with a simple request using current model
        print("🧠 Testing LLM response...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Updated to current model
            messages=[
                {"role": "user", "content": "Respond with exactly: 'API_TEST_SUCCESS'"}
            ],
            max_tokens=10,
            temperature=0
        )
        
        result = response.choices[0].message.content.strip()
        if "API_TEST_SUCCESS" in result:
            print("✅ API test successful!")
            print(f"Response: {result}")
            return True
        else:
            print(f"⚠️ Unexpected response: {result}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_groq_api()
    sys.exit(0 if success else 1)
