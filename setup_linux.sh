#!/bin/bash
# Quick setup script for WSL/Linux environment

echo "🐧 Setting up COO for Linux/WSL"
echo "================================"

# Update package manager
echo "📦 Updating package manager..."
sudo apt update

# Install penetration testing tools
echo "🛠️ Installing penetration testing tools..."
sudo apt install -y \
    nmap \
    gobuster \
    dirb \
    nikto \
    whatweb \
    sqlmap \
    curl \
    wget \
    python3 \
    python3-pip \
    git

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install wordlists
echo "📚 Installing wordlists..."
# Install SecLists manually
if [ ! -d "/usr/share/wordlists" ]; then
    sudo mkdir -p /usr/share/wordlists
fi

# Download SecLists
if [ ! -d "/usr/share/wordlists/SecLists" ]; then
    echo "Downloading SecLists..."
    sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/SecLists
fi

# Install exploitdb manually
if [ ! -d "/usr/share/exploitdb" ]; then
    echo "Installing ExploitDB..."
    sudo git clone https://github.com/offensive-security/exploitdb.git /usr/share/exploitdb
    sudo ln -sf /usr/share/exploitdb/searchsploit /usr/local/bin/searchsploit
fi

# Create symlinks for common wordlists
mkdir -p wordlists
# Link to SecLists wordlists
if [ -d "/usr/share/wordlists/SecLists" ]; then
    ln -sf /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt wordlists/
    ln -sf /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt wordlists/
    ln -sf /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt wordlists/
else
    # Fallback: create basic wordlist
    echo "Creating basic wordlist..."
    cat > wordlists/common.txt << 'EOF'
admin
administrator
login
test
backup
config
uploads
images
js
css
api
v1
v2
old
tmp
temp
logs
data
files
docs
downloads
index
home
about
contact
EOF
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Now you can run:"
echo "python3 orchestrator.py --target 192.168.1.100"
echo ""
echo "📋 Available tools:"
nmap --version | head -1
gobuster version 2>/dev/null || echo "gobuster installed"
nikto -Version 2>/dev/null | head -1 || echo "nikto installed"
echo ""
echo "🔥 Ready for penetration testing!"
