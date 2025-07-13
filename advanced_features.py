#!/usr/bin/env python3
"""
Advanced features and extensions for the Cybersecurity Operations Orchestrator
"""

import json
import threading
import time
import queue
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

class NotificationManager:
    """Handles notifications for completed scans and critical findings"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.webhook_url = config.get("webhook_url", "")
        self.email_config = config.get("email", {})
        
    def send_notification(self, title: str, message: str, severity: str = "info"):
        """Send notification via configured methods"""
        if not self.enabled:
            return
            
        # Send webhook notification
        if self.webhook_url:
            self._send_webhook(title, message, severity)
            
        # Send email notification
        if self.email_config.get("enabled", False):
            self._send_email(title, message, severity)
    
    def _send_webhook(self, title: str, message: str, severity: str):
        """Send webhook notification (e.g., Slack, Discord, Teams)"""
        try:
            import requests
            payload = {
                "title": title,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now().isoformat()
            }
            
            requests.post(self.webhook_url, json=payload, timeout=10)
            logging.info("Webhook notification sent successfully")
        except Exception as e:
            logging.error(f"Failed to send webhook notification: {e}")
    
    def _send_email(self, title: str, message: str, severity: str):
        """Send email notification"""
        try:
            smtp_server = self.email_config.get("smtp_server")
            smtp_port = self.email_config.get("smtp_port", 587)
            username = self.email_config.get("username")
            password = self.email_config.get("password")
            to_email = self.email_config.get("to_email")
            
            if not all([smtp_server, username, password, to_email]):
                logging.warning("Incomplete email configuration")
                return
            
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = to_email
            msg['Subject'] = f"COO Alert: {title}"
            
            body = f"""
Cybersecurity Operations Orchestrator Alert

Title: {title}
Severity: {severity}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message:
{message}

This is an automated notification from the COO system.
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            logging.info("Email notification sent successfully")
        except Exception as e:
            logging.error(f"Failed to send email notification: {e}")

class RealTimeMonitor:
    """Real-time monitoring of the penetration test progress"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.stats = {
            "start_time": datetime.now(),
            "commands_executed": 0,
            "ports_discovered": 0,
            "vulnerabilities_found": 0,
            "directories_found": 0,
            "current_phase": "initialization"
        }
        self.running = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start the real-time monitoring"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop the real-time monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def update_stats(self, state: Dict[str, Any], phase: str = None):
        """Update monitoring statistics"""
        self.stats["commands_executed"] += 1
        self.stats["ports_discovered"] = len(state.get("open_ports", []))
        self.stats["vulnerabilities_found"] = len(state.get("vulnerabilities", []))
        self.stats["directories_found"] = len(state.get("web_directories", []))
        
        if phase:
            self.stats["current_phase"] = phase
            
        # Save stats to file
        stats_file = self.output_dir / "real_time_stats.json"
        with open(stats_file, 'w') as f:
            json.dump({
                **self.stats,
                "start_time": self.stats["start_time"].isoformat(),
                "last_update": datetime.now().isoformat()
            }, f, indent=2)
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.running:
            # Generate real-time status
            runtime = datetime.now() - self.stats["start_time"]
            
            status = f"""
╭─ COO Real-Time Status ─────────────────────────────╮
│ Runtime: {str(runtime).split('.')[0]:<42} │
│ Phase: {self.stats['current_phase']:<44} │
│ Commands: {self.stats['commands_executed']:<41} │
│ Ports Found: {self.stats['ports_discovered']:<38} │
│ Vulnerabilities: {self.stats['vulnerabilities_found']:<34} │
│ Directories: {self.stats['directories_found']:<38} │
╰────────────────────────────────────────────────────╯
"""
            
            # Clear screen and show status (works on most terminals)
            print("\033[2J\033[H" + status)
            
            time.sleep(5)  # Update every 5 seconds

class VulnerabilityDatabase:
    """Local vulnerability database for quick lookups"""
    
    def __init__(self, db_file: str = "vulnerability_db.json"):
        self.db_file = Path(db_file)
        self.db = self._load_database()
        
    def _load_database(self) -> Dict[str, Any]:
        """Load vulnerability database"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_database()
    
    def _create_default_database(self) -> Dict[str, Any]:
        """Create a default vulnerability database"""
        default_db = {
            "services": {
                "apache": {
                    "2.4.41": {
                        "cves": ["CVE-2021-41773", "CVE-2021-42013"],
                        "description": "Path traversal vulnerabilities",
                        "severity": "high"
                    },
                    "2.4.49": {
                        "cves": ["CVE-2021-41773"],
                        "description": "Path traversal vulnerability",
                        "severity": "high"
                    }
                },
                "openssh": {
                    "7.4": {
                        "cves": ["CVE-2018-15473"],
                        "description": "Username enumeration vulnerability",
                        "severity": "medium"
                    },
                    "8.2p1": {
                        "cves": [],
                        "description": "Generally secure version",
                        "severity": "low"
                    }
                }
            },
            "ports": {
                "21": {
                    "service": "ftp",
                    "common_vulns": ["Anonymous login", "Directory traversal"],
                    "enumeration_commands": ["nmap -sV -sC -p 21", "ftp anonymous login"]
                },
                "22": {
                    "service": "ssh",
                    "common_vulns": ["Weak credentials", "Version vulnerabilities"],
                    "enumeration_commands": ["ssh-audit", "nmap --script ssh-auth-methods"]
                },
                "80": {
                    "service": "http",
                    "common_vulns": ["Directory traversal", "SQL injection", "XSS"],
                    "enumeration_commands": ["gobuster", "nikto", "whatweb"]
                }
            }
        }
        
        # Save default database
        with open(self.db_file, 'w') as f:
            json.dump(default_db, f, indent=2)
            
        return default_db
    
    def lookup_service_vulnerabilities(self, service: str, version: str) -> List[Dict[str, Any]]:
        """Lookup vulnerabilities for a specific service and version"""
        service_lower = service.lower()
        service_data = self.db.get("services", {}).get(service_lower, {})
        
        vulnerabilities = []
        for ver, vuln_data in service_data.items():
            if version and ver in version:
                vulnerabilities.append({
                    "service": service,
                    "version": version,
                    "cves": vuln_data.get("cves", []),
                    "description": vuln_data.get("description", ""),
                    "severity": vuln_data.get("severity", "unknown")
                })
        
        return vulnerabilities
    
    def get_port_info(self, port: int) -> Dict[str, Any]:
        """Get information about a specific port"""
        return self.db.get("ports", {}).get(str(port), {})

class ReportExporter:
    """Export reports in various formats"""
    
    @staticmethod
    def export_to_json(state: Dict[str, Any], output_file: str):
        """Export penetration test results to JSON"""
        with open(output_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    @staticmethod
    def export_to_csv(state: Dict[str, Any], output_file: str):
        """Export findings to CSV format"""
        import csv
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Type', 'Port', 'Service', 'Version', 'Vulnerability', 'Severity'])
            
            # Write port information
            for port_info in state.get("open_ports", []):
                writer.writerow([
                    'Port',
                    port_info.get("port", ""),
                    port_info.get("service", ""),
                    port_info.get("version", ""),
                    "",
                    ""
                ])
            
            # Write vulnerabilities
            for vuln in state.get("vulnerabilities", []):
                writer.writerow([
                    'Vulnerability',
                    vuln.get("port", ""),
                    "",
                    "",
                    vuln.get("description", ""),
                    vuln.get("severity", "")
                ])
    
    @staticmethod
    def export_to_html(state: Dict[str, Any], output_file: str):
        """Export to HTML report"""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Penetration Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background-color: #f4f4f4; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .port { background-color: #e8f4f8; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .vulnerability { background-color: #ffe8e8; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .high-severity { border-left: 5px solid #d32f2f; }
        .medium-severity { border-left: 5px solid #f57c00; }
        .low-severity { border-left: 5px solid #388e3c; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Penetration Test Report</h1>
        <p><strong>Target:</strong> {target_ip}</p>
        <p><strong>Date:</strong> {date}</p>
    </div>
    
    <div class="section">
        <h2>Open Ports</h2>
        {ports_html}
    </div>
    
    <div class="section">
        <h2>Vulnerabilities</h2>
        {vulnerabilities_html}
    </div>
    
    <div class="section">
        <h2>Web Directories</h2>
        <ul>
        {directories_html}
        </ul>
    </div>
</body>
</html>
"""
        
        # Generate ports HTML
        ports_html = ""
        for port_info in state.get("open_ports", []):
            ports_html += f"""
            <div class="port">
                <strong>Port {port_info.get('port', 'Unknown')}:</strong> 
                {port_info.get('service', 'Unknown')} 
                ({port_info.get('version', 'Unknown version')})
            </div>
            """
        
        # Generate vulnerabilities HTML
        vulnerabilities_html = ""
        for vuln in state.get("vulnerabilities", []):
            severity = vuln.get("severity", "unknown")
            severity_class = f"{severity}-severity" if severity in ["high", "medium", "low"] else ""
            vulnerabilities_html += f"""
            <div class="vulnerability {severity_class}">
                <strong>{vuln.get('cve', 'Unknown CVE')}:</strong> 
                {vuln.get('description', 'No description')}
                <br><small>Port: {vuln.get('port', 'Unknown')}, Severity: {severity}</small>
            </div>
            """
        
        # Generate directories HTML
        directories_html = ""
        for directory in state.get("web_directories", []):
            directories_html += f"<li>{directory}</li>"
        
        # Fill template
        html_content = html_template.format(
            target_ip=state.get("target_ip", "Unknown"),
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ports_html=ports_html,
            vulnerabilities_html=vulnerabilities_html,
            directories_html=directories_html
        )
        
        with open(output_file, 'w') as f:
            f.write(html_content)

class AdvancedOrchestrator:
    """Extended orchestrator with advanced features"""
    
    def __init__(self, base_orchestrator, config_file: str = "advanced_config.json"):
        self.base = base_orchestrator
        self.config = self._load_config(config_file)
        
        # Initialize advanced components
        self.notification_manager = NotificationManager(
            self.config.get("notifications", {})
        )
        self.vulnerability_db = VulnerabilityDatabase()
        self.monitor = RealTimeMonitor(base_orchestrator.output_dir)
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load advanced configuration"""
        config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            return {}
    
    def enhanced_analysis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Perform enhanced analysis with vulnerability database lookup"""
        enhanced_state = state.copy()
        
        # Lookup vulnerabilities for discovered services
        for port_info in enhanced_state.get("open_ports", []):
            service = port_info.get("service", "")
            version = port_info.get("version", "")
            
            if service and version:
                vulns = self.vulnerability_db.lookup_service_vulnerabilities(service, version)
                for vuln in vulns:
                    enhanced_state.setdefault("vulnerabilities", []).append({
                        "port": port_info["port"],
                        "cve": ", ".join(vuln["cves"]),
                        "description": vuln["description"],
                        "severity": vuln["severity"]
                    })
        
        return enhanced_state
    
    def run_with_monitoring(self):
        """Run orchestrator with real-time monitoring"""
        self.monitor.start_monitoring()
        
        try:
            # Send start notification
            self.notification_manager.send_notification(
                "Penetration Test Started",
                f"Target: {self.base.target_ip}",
                "info"
            )
            
            # Run the base orchestrator (would need integration)
            # self.base.run_penetration_test()
            
        finally:
            self.monitor.stop_monitoring()
            
            # Send completion notification
            self.notification_manager.send_notification(
                "Penetration Test Completed",
                f"Target: {self.base.target_ip}, Commands: {self.monitor.stats['commands_executed']}",
                "info"
            )

def create_advanced_config():
    """Create advanced configuration file"""
    config = {
        "notifications": {
            "enabled": True,
            "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "your-email@gmail.com",
                "password": "your-app-password",
                "to_email": "recipient@example.com"
            }
        },
        "monitoring": {
            "real_time": True,
            "update_interval": 5,
            "save_stats": True
        },
        "vulnerability_database": {
            "enabled": True,
            "auto_update": False,
            "sources": [
                "https://cve.mitre.org/data/downloads/",
                "https://nvd.nist.gov/feeds/json/cve/1.1/"
            ]
        },
        "reporting": {
            "formats": ["markdown", "json", "html", "csv"],
            "auto_export": True,
            "include_raw_output": False
        }
    }
    
    config_file = Path("advanced_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Advanced configuration saved to: {config_file}")

if __name__ == "__main__":
    create_advanced_config()
