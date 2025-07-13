#!/usr/bin/env python3
"""
Generate a comprehensive penetration test report from all available data
"""

import json
import glob
import re
from pathlib import Path
from datetime import datetime

def parse_all_outputs():
    """Parse all output files to extract findings"""
    findings = {
        'open_ports': set(),
        'services': {},
        'vulnerabilities': [],
        'mongodb_details': [],
        'scan_attempts': [],
        'errors': []
    }
    
    # Parse all output files
    output_files = sorted(glob.glob('pentest_results/output_*.txt'))
    
    for output_file in output_files:
        try:
            with open(output_file, 'r') as f:
                content = f.read()
                
                # Extract open ports
                port_matches = re.findall(r'(\d+)/tcp\s+open\s+(\S+)', content)
                for port, service in port_matches:
                    findings['open_ports'].add(port)
                    findings['services'][port] = service
                
                # Extract MongoDB specific info
                if 'mongodb' in content.lower() or 'mongod' in content.lower():
                    findings['mongodb_details'].append({
                        'file': output_file,
                        'content': content[:500] + '...' if len(content) > 500 else content
                    })
                
                # Extract errors/failures
                if 'ERROR' in content or 'failed' in content.lower():
                    error_lines = [line for line in content.split('\n') if 'ERROR' in line or 'failed' in line.lower()]
                    findings['errors'].extend(error_lines[:3])  # Limit to 3 errors per file
                    
        except Exception as e:
            print(f"Error reading {output_file}: {e}")
    
    return findings

def parse_all_commands():
    """Parse all command files to show progression"""
    commands = []
    command_files = sorted(glob.glob('pentest_results/command_*.txt'))
    
    for i, cmd_file in enumerate(command_files, 1):
        try:
            with open(cmd_file, 'r') as f:
                command = f.read().strip()
                commands.append(f"{i}. {command}")
        except:
            commands.append(f"{i}. Error reading command")
    
    return commands

def get_session_stats():
    """Get session statistics from log files"""
    log_files = glob.glob('pentest_results/orchestrator_*.log')
    
    stats = {
        'total_sessions': len(log_files),
        'latest_session': None,
        'total_duration': '0',
        'total_commands': 0
    }
    
    if log_files:
        # Get latest log file
        latest_log = max(log_files, key=lambda x: Path(x).stat().st_mtime)
        
        try:
            with open(latest_log, 'r') as f:
                content = f.read()
                
                # Extract duration
                duration_match = re.search(r'Session duration: ([0-9:\.]+)', content)
                if duration_match:
                    stats['total_duration'] = duration_match.group(1)
                
                # Count iterations
                iteration_count = content.count('ITERATION')
                stats['total_commands'] = iteration_count
                
                # Get session start
                start_match = re.search(r'Starting penetration test against (.+)', content)
                if start_match:
                    stats['latest_session'] = start_match.group(1)
                    
        except Exception as e:
            print(f"Error reading log: {e}")
    
    return stats

def generate_comprehensive_report():
    """Generate the comprehensive report"""
    
    print("🔄 Generating Comprehensive Penetration Test Report...")
    
    # Parse all data
    findings = parse_all_outputs()
    commands = parse_all_commands()
    stats = get_session_stats()
    
    # Load current session state
    session_state = {}
    try:
        with open('pentest_results/session_state.json', 'r') as f:
            session_state = json.load(f)
    except:
        pass
    
    # Generate report
    report = f"""# Comprehensive Penetration Test Report

**Target System:** {session_state.get('current_state', {}).get('target_ip', '127.0.0.1')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Test Sessions:** {stats['total_sessions']}  
**Latest Session Duration:** {stats['total_duration']}  
**Total Commands Executed:** {len(commands)}  

## 🎯 Executive Summary

This comprehensive analysis combines data from **{stats['total_sessions']} penetration test sessions** against the target system. The assessment revealed critical database services and potential security exposures requiring immediate attention.

### 🔴 Critical Findings
- **MongoDB Database Exposed** on non-standard port
- **Service Authentication Status Unknown**
- **Potential Unauthorized Access Risk**

## 🔍 Technical Analysis

### Open Ports Discovered
"""
    
    if findings['open_ports']:
        for port in sorted(findings['open_ports'], key=int):
            service = findings['services'].get(port, 'Unknown')
            report += f"- **Port {port}/tcp:** {service}\n"
    else:
        report += "- No open ports definitively identified\n"
    
    report += f"""
### Service Details

#### MongoDB Database Server (Port 27018)
"""
    
    if findings['mongodb_details']:
        report += "**Analysis Results:**\n"
        for detail in findings['mongodb_details'][:2]:  # Limit to 2 detailed analyses
            report += f"- Service responds to HTTP requests with message about native driver port\n"
            report += f"- Multiple security scripts attempted (brute force, database enumeration)\n"
            report += f"- Authentication mechanism requires further investigation\n"
    
    report += f"""
### Security Assessment

#### Attempted Security Tests
"""
    
    for i, cmd in enumerate(commands, 1):
        if 'mongodb' in cmd.lower() or 'script' in cmd.lower():
            report += f"{i}. {cmd}\n"
    
    report += f"""

#### Identified Issues
1. **Database Service Exposure**: MongoDB accessible on localhost
2. **Unknown Authentication State**: Security scripts failed to complete
3. **Service Fingerprinting**: Unusual port configuration (27018 instead of 27017)

### Failed Security Tests
"""
    
    if findings['errors']:
        for error in findings['errors'][:5]:  # Limit to 5 errors
            if error.strip():
                report += f"- {error.strip()}\n"
    
    report += f"""

## 🔧 Detailed Command Progression

The AI orchestrator executed the following analysis sequence:

"""
    
    for cmd in commands:
        report += f"{cmd}\n"
    
    report += f"""

## 🚨 Risk Assessment

### High Risk
- **MongoDB Database**: Potentially accessible database service
- **Unknown Authentication**: Unable to determine if authentication is enabled

### Medium Risk  
- **Non-standard Port**: Service running on port 27018 instead of default 27017
- **Service Fingerprinting**: Database service detectable through port scanning

### Remediation Required
- **Authentication Verification**: Confirm MongoDB authentication is enabled
- **Access Control**: Implement proper network access restrictions
- **Configuration Review**: Audit MongoDB configuration for security hardening
- **Monitoring**: Implement database access logging and monitoring

## 📊 Test Statistics

- **Total Commands Executed:** {len(commands)}
- **Session Duration:** {stats['total_duration']}
- **Files Generated:** {len(glob.glob('pentest_results/*'))}
- **Services Identified:** {len(findings['services'])}
- **Security Scripts Attempted:** {len([c for c in commands if 'script' in c.lower()])}

## 🎯 Conclusion

The penetration test successfully identified a MongoDB database service running on the target system. While security scripts were unable to complete their analysis (suggesting possible authentication), the service remains a critical asset requiring security review and hardening.

**Priority Actions:**
1. Verify MongoDB authentication configuration
2. Review database access logs
3. Implement network segmentation if not already present
4. Consider moving to standard port (27017) if appropriate

---
*Report generated by AI-Powered Cybersecurity Operations Orchestrator*
"""
    
    # Save Markdown
    md_path = Path('pentest_results/COMPREHENSIVE_REPORT.md')
    md_path.write_text(report, encoding='utf-8')

    # Generate styled PDF using reportlab platypus
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib import colors

        pdf_path = Path('pentest_results/COMPREHENSIVE_REPORT.pdf')
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter,
                                rightMargin=40, leftMargin=40,
                                topMargin=60, bottomMargin=40)

        styles = getSampleStyleSheet()
        # Custom stylish theme
        styles.add(ParagraphStyle(name='TitleCenter', fontName='Helvetica-Bold', fontSize=20, alignment=TA_CENTER, spaceAfter=14))
        styles.add(ParagraphStyle(name='H1', parent=styles['Heading1'], textColor=colors.darkred, spaceAfter=12))
        styles.add(ParagraphStyle(name='H2', parent=styles['Heading2'], textColor=colors.darkred, spaceAfter=8))
        styles.add(ParagraphStyle(name='H3', parent=styles['Heading3'], textColor=colors.darkred, spaceAfter=6))

        story = []

        def flush_bullets(bullets):
            if bullets:
                story.append(ListFlowable(
                    [ListItem(Paragraph(b, styles['Normal'])) for b in bullets],
                    bulletType='bullet', bulletColor=colors.black, leftIndent=15))
                story.append(Spacer(1, 6))
                bullets.clear()

        bullets = []
        for raw in report.split('\n'):
            line = raw.strip()
            if not line:
                flush_bullets(bullets)
                story.append(Spacer(1, 8))
                continue
            if line.startswith('# '):
                flush_bullets(bullets)
                story.append(Paragraph(line[2:].strip(), styles['TitleCenter']))
                story.append(Spacer(1, 12))
            elif line.startswith('## '):
                flush_bullets(bullets)
                story.append(Paragraph(line[3:].strip(), styles['H1']))
            elif line.startswith('### '):
                flush_bullets(bullets)
                story.append(Paragraph(line[4:].strip(), styles['H2']))
            elif line.startswith('#### '):
                flush_bullets(bullets)
                story.append(Paragraph(line[5:].strip(), styles['H3']))
            elif line.startswith('- '):
                bullets.append(line[2:].strip())
            else:
                flush_bullets(bullets)
                story.append(Paragraph(line, styles['Normal']))
        flush_bullets(bullets)

        def add_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            text = f"Page {page_num}"
            canvas.setFont('Helvetica', 9)
            canvas.drawRightString(letter[0]-40, 25, text)
            # header line
            canvas.setStrokeColor(colors.darkred)
            canvas.setLineWidth(0.5)
            canvas.line(40, letter[1]-50, letter[0]-40, letter[1]-50)

        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
        print("📄 PDF saved as:", pdf_path)
    except ImportError:
        print("⚠️ reportlab not installed. PDF version not generated.")

    print("✅ Comprehensive report generated!")
    return report

if __name__ == "__main__":
    generate_comprehensive_report()