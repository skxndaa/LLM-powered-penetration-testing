# 🐧 Linux/WSL Setup Guide for COO

## Why Use Linux/WSL?

You're absolutely correct! Penetration testing tools are designed for Linux environments:

- **nmap**: Native Linux tool, Windows version has limitations
- **gobuster**: Go-based tool, works best on Linux
- **nikto**: Perl-based web scanner, optimized for Unix
- **sqlmap**: Python tool, better library support on Linux
- **Metasploit**: Ruby framework, native Linux support

## 🚀 Quick Setup Options

### Option 1: WSL2 (Recommended for Windows users)

1. **Install WSL2:**
   ```powershell
   # Run in PowerShell as Administrator
   wsl --install -d Ubuntu
   ```

2. **Setup COO in WSL:**
   ```bash
   # In WSL Ubuntu terminal
   cd /mnt/c/Users/rexjo/soc_gen
   chmod +x setup_linux.sh
   ./setup_linux.sh
   ```

3. **Run the orchestrator:**
   ```bash
   python3 orchestrator.py --target 127.0.0.1
   ```

### Option 2: Kali Linux (Best for pentesting)

1. **Download Kali Linux:**
   - VM: https://www.kali.org/get-kali/
   - WSL: `wsl --install -d kali-linux`

2. **Everything pre-installed:**
   ```bash
   # All tools already available
   nmap --version
   gobuster version
   nikto -Version
   ```

### Option 3: Docker Kali

```bash
# Run Kali in Docker
docker run -it --rm -v $(pwd):/workspace kalilinux/kali-rolling
cd /workspace
apt update && apt install -y kali-tools-top10
```

## 🎯 Why This Makes a Difference

### Linux/WSL Performance:
```bash
# Linux nmap (fast, full features)
nmap -sS -O -sV -p- target.com

# Windows equivalent (limited, slower)
# Many advanced features don't work
```

### Tool Availability:
```bash
# Linux: One command installs everything
sudo apt install kali-tools-top10

# Windows: Manual installation, compatibility issues
# Many tools simply don't work properly
```

## 🔥 Recommended Workflow

1. **Use WSL2 Ubuntu** for development and testing
2. **Copy your COO project to WSL:**
   ```bash
   cp -r /mnt/c/Users/rexjo/soc_gen ~/coo
   cd ~/coo
   ```

3. **Run the Linux setup:**
   ```bash
   chmod +x setup_linux.sh
   ./setup_linux.sh
   ```

4. **Test with real tools:**
   ```bash
   python3 orchestrator.py --target 127.0.0.1
   ```

## 🛡️ Professional Pentesting Environment

For serious penetration testing, professionals use:

- **Kali Linux** (most popular)
- **ParrotOS** (privacy-focused)
- **BlackArch Linux** (comprehensive tool set)
- **Pentoo** (Gentoo-based)

All of these come with COO-compatible tools pre-installed.

## 💡 Quick Start with WSL

If you want to get started right now:

```powershell
# 1. Install WSL2 (if not already installed)
wsl --install

# 2. Open Ubuntu terminal
wsl

# 3. Navigate to your project
cd /mnt/c/Users/rexjo/soc_gen

# 4. Run Linux setup
chmod +x setup_linux.sh
./setup_linux.sh

# 5. Test the orchestrator
python3 orchestrator.py --target 127.0.0.1
```

You'll immediately see the difference in tool availability and performance! 🚀
