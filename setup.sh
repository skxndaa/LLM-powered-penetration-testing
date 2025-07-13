#!/bin/bash

# Cybersecurity Operations Orchestrator - Setup Script for Linux/macOS
# This script installs required tools and dependencies

set -e

echo "🔧 Cybersecurity Operations Orchestrator Setup"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. Some tools may not install correctly."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/debian_version ]; then
            OS="debian"
        elif [ -f /etc/redhat-release ]; then
            OS="redhat"
        elif [ -f /etc/arch-release ]; then
            OS="arch"
        else
            OS="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    
    print_status "Detected OS: $OS"
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_error "pip not found. Please install Python 3 and pip first."
        exit 1
    fi
    
    # Use pip3 if available, otherwise pip
    PIP_CMD="pip3"
    if ! command -v pip3 &> /dev/null; then
        PIP_CMD="pip"
    fi
    
    $PIP_CMD install -r requirements.txt
    print_status "Python dependencies installed successfully"
}

# Install penetration testing tools for Debian/Ubuntu
install_tools_debian() {
    print_status "Installing penetration testing tools for Debian/Ubuntu..."
    
    sudo apt update
    
    # Core tools
    sudo apt install -y \
        nmap \
        gobuster \
        dirb \
        nikto \
        whatweb \
        sqlmap \
        exploitdb \
        searchsploit \
        curl \
        wget \
        git
    
    # Metasploit Framework
    if ! command -v msfconsole &> /dev/null; then
        print_status "Installing Metasploit Framework..."
        curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
        chmod 755 msfinstall
        sudo ./msfinstall
        rm msfinstall
    fi
    
    # Wordlists
    print_status "Installing wordlists..."
    sudo apt install -y seclists
    
    print_status "Debian/Ubuntu tools installation completed"
}

# Install penetration testing tools for Red Hat/CentOS/Fedora
install_tools_redhat() {
    print_status "Installing penetration testing tools for Red Hat/CentOS/Fedora..."
    
    # Enable EPEL repository for CentOS/RHEL
    if command -v yum &> /dev/null; then
        sudo yum install -y epel-release
        sudo yum update -y
        sudo yum install -y nmap curl wget git
    elif command -v dnf &> /dev/null; then
        sudo dnf update -y
        sudo dnf install -y nmap curl wget git
    fi
    
    # Many tools need to be installed manually or from source on RHEL
    print_warning "Some tools may need manual installation on Red Hat systems"
    print_status "Basic tools installed. Consider using Kali Linux for full tool availability."
}

# Install penetration testing tools for Arch Linux
install_tools_arch() {
    print_status "Installing penetration testing tools for Arch Linux..."
    
    sudo pacman -Syu --noconfirm
    sudo pacman -S --noconfirm \
        nmap \
        gobuster \
        dirb \
        nikto \
        sqlmap \
        curl \
        wget \
        git
    
    # Install from AUR if available
    print_status "Some tools may need to be installed from AUR"
}

# Install penetration testing tools for macOS
install_tools_macos() {
    print_status "Installing penetration testing tools for macOS..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        print_status "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install tools via Homebrew
    brew update
    brew install \
        nmap \
        gobuster \
        dirb \
        nikto \
        sqlmap \
        wget \
        curl
    
    print_status "macOS tools installation completed"
}

# Create directories and sample files
setup_directories() {
    print_status "Setting up directories and sample files..."
    
    # Create wordlists directory
    mkdir -p wordlists
    
    # Create sample wordlist if no wordlists exist
    if [ ! -f "wordlists/common.txt" ]; then
        cat > wordlists/common.txt << EOF
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
services
products
news
blog
forum
search
help
support
faq
EOF
        print_status "Created sample wordlist: wordlists/common.txt"
    fi
    
    # Create results directory
    mkdir -p pentest_results
    
    print_status "Directory setup completed"
}

# Verify tool installation
verify_tools() {
    print_status "Verifying tool installation..."
    
    tools=("nmap" "gobuster" "dirb" "nikto" "sqlmap" "curl" "wget")
    missing_tools=()
    
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            echo "  ✓ $tool"
        else
            echo "  ✗ $tool"
            missing_tools+=("$tool")
        fi
    done
    
    # Optional tools
    optional_tools=("whatweb" "searchsploit" "msfconsole")
    print_status "Optional tools:"
    
    for tool in "${optional_tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            echo "  ✓ $tool"
        else
            echo "  ✗ $tool (optional)"
        fi
    done
    
    if [ ${#missing_tools[@]} -eq 0 ]; then
        print_status "All core tools are available!"
    else
        print_warning "Missing tools: ${missing_tools[*]}"
        print_warning "The orchestrator may have limited functionality"
    fi
}

# Create sample configuration
create_sample_config() {
    print_status "Creating sample configuration..."
    
    cat > sample_config.sh << 'EOF'
#!/bin/bash

# Sample configuration for COO
# Copy this file to config.sh and customize as needed

# Groq API Configuration
export GROQ_API_KEY="your_groq_api_key_here"

# Default target (can be overridden via command line)
export DEFAULT_TARGET="192.168.1.100"

# Tool paths (customize if tools are not in PATH)
export NMAP_PATH="nmap"
export GOBUSTER_PATH="gobuster"
export DIRB_PATH="dirb"
export NIKTO_PATH="nikto"
export SQLMAP_PATH="sqlmap"

# Wordlist paths
export WORDLIST_DIR="wordlists"
export COMMON_WORDLIST="$WORDLIST_DIR/common.txt"

# Output configuration
export OUTPUT_DIR="pentest_results"
export MAX_ITERATIONS=50

# Notification settings (optional)
export ENABLE_NOTIFICATIONS=false
export SLACK_WEBHOOK_URL=""
export EMAIL_NOTIFICATIONS=false

echo "Configuration loaded successfully"
EOF
    
    chmod +x sample_config.sh
    print_status "Created sample_config.sh"
}

# Main installation function
main() {
    print_status "Starting COO setup..."
    
    check_root
    detect_os
    
    # Install Python dependencies
    install_python_deps
    
    # Install tools based on OS
    case $OS in
        "debian")
            install_tools_debian
            ;;
        "redhat")
            install_tools_redhat
            ;;
        "arch")
            install_tools_arch
            ;;
        "macos")
            install_tools_macos
            ;;
        *)
            print_warning "Unknown OS. Please install tools manually:"
            echo "  - nmap, gobuster, dirb, nikto, sqlmap, curl, wget"
            ;;
    esac
    
    # Setup directories
    setup_directories
    
    # Create sample configuration
    create_sample_config
    
    # Verify installation
    verify_tools
    
    print_status "Setup completed!"
    echo
    echo "Next steps:"
    echo "1. Get your Groq API key from: https://console.groq.com/"
    echo "2. Edit sample_config.sh with your API key and settings"
    echo "3. Run: python3 orchestrator.py --target <TARGET_IP> --groq-api-key <YOUR_KEY>"
    echo
    echo "For testing: python3 examples.py dry-run"
    echo
    print_warning "Remember: Only test systems you own or have explicit permission to test!"
}

# Run main function
main "$@"
