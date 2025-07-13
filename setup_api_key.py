#!/usr/bin/env python3
"""
Simple setup utility for configuring the Groq API key
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def main():
    print("🔑 Groq API Key Configuration")
    print("=" * 40)
    
    # Check if API key already exists
    existing_key = ""
    
    # Check environment variable
    env_key = os.environ.get('GROQ_API_KEY')
    if env_key:
        print(f"✓ Found API key in environment variable")
        existing_key = env_key[:10] + "..." if len(env_key) > 10 else env_key
    
    # Check config file
    config_file = Path('groq_config.json')
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                file_key = config_data.get('api_key', '')
                if file_key:
                    print(f"✓ Found API key in config file")
                    existing_key = file_key[:10] + "..." if len(file_key) > 10 else file_key
        except:
            pass
    
    if existing_key:
        print(f"Current key: {existing_key}")
        response = input("Do you want to update it? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("No changes made.")
            return
    
    print("\nTo get your Groq API key:")
    print("1. Go to: https://console.groq.com/")
    print("2. Sign up or log in")
    print("3. Go to API Keys section")
    print("4. Create a new API key")
    print()
    
    # Get new API key
    while True:
        api_key = input("Enter your Groq API key: ").strip()
        
        if not api_key:
            print("❌ API key cannot be empty")
            continue
            
        if len(api_key) < 20:
            print("❌ API key seems too short")
            retry = input("Continue anyway? (y/N): ").strip().lower()
            if retry not in ['y', 'yes']:
                continue
        
        break
    
    # Choose storage method
    print("\nHow would you like to store your API key?")
    print("1. Config file (groq_config.json) - Convenient")
    print("2. Environment variable - More secure")
    print("3. Both - Maximum convenience")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            save_to_config_file(api_key)
            break
        elif choice == "2":
            save_to_environment(api_key)
            break
        elif choice == "3":
            save_to_config_file(api_key)
            save_to_environment(api_key)
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    print("\n✅ Configuration complete!")
    print("\nYou can now run the orchestrator with:")
    print("python orchestrator.py --target 192.168.1.100")
    print("(No need to specify --groq-api-key anymore)")

def save_to_config_file(api_key: str):
    """Save API key to config file"""
    config_file = Path('groq_config.json')
    config_data = {
        'api_key': api_key,
        'created': datetime.now().isoformat()
    }
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        print(f"✓ API key saved to {config_file}")
        print("⚠️  Keep this file secure and don't share it!")
        
        # Add to .gitignore if it exists
        gitignore = Path('.gitignore')
        if gitignore.exists():
            with open(gitignore, 'r') as f:
                content = f.read()
            if 'groq_config.json' not in content:
                with open(gitignore, 'a') as f:
                    f.write('\n# Groq API configuration\ngroq_config.json\n')
                print("✓ Added groq_config.json to .gitignore")
        else:
            with open(gitignore, 'w') as f:
                f.write('# Groq API configuration\ngroq_config.json\n')
            print("✓ Created .gitignore with groq_config.json")
            
    except Exception as e:
        print(f"❌ Failed to save config file: {e}")

def save_to_environment(api_key: str):
    """Show instructions for setting environment variable"""
    print(f"\n✓ To set environment variable, run:")
    
    if os.name == 'nt':  # Windows
        print(f"PowerShell:")
        print(f'$env:GROQ_API_KEY = "{api_key}"')
        print(f"\nCommand Prompt:")
        print(f'set GROQ_API_KEY={api_key}')
        print(f"\nTo make it permanent, add it to your system environment variables.")
    else:  # Unix-like
        print(f"Bash/Zsh:")
        print(f'export GROQ_API_KEY="{api_key}"')
        print(f"\nTo make it permanent, add the above line to your ~/.bashrc or ~/.zshrc")

if __name__ == "__main__":
    main()
