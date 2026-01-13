"""
Email Alert Notifier
Sends daily digest emails via Gmail SMTP
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from datetime import datetime


class EmailNotifier:
    """Send email notifications via Gmail SMTP"""
    
    def __init__(self, email_user: str = None, email_password: str = None):
        """
        Initialize email notifier
        
        Args:
            email_user: Gmail address (from environment if not provided)
            email_password: Gmail app password (from environment if not provided)
        """
        self.email_user = email_user or os.getenv('EMAIL_USER')
        self.email_password = email_password or os.getenv('EMAIL_PASSWORD')
        self.dry_run = not (self.email_user and self.email_password)
        
        if self.dry_run:
            print("⚠️ Warning: EMAIL_USER or EMAIL_PASSWORD not set. Emails in dry-run mode")
        
        self.sent_emails = []
    
    def send_alert_email(self, alert: Dict, recipient: str) -> bool:
        """
        Send immediate alert email
        
        Args:
            alert: Alert dict
            recipient: Recipient email address
        
        Returns:
            True if sent successfully
        """
        
        subject = f"🚨 Alert: {alert['activity_name']} - {alert['status'].upper()}"
        html = self._build_alert_html(alert)
        
        return self._send_email(
            to_email=recipient,
            subject=subject,
            html_content=html
        )
    
    def send_daily_digest(self, alerts_data: Dict, recipients: List[str]) -> Dict:
        """
        Send daily digest email to recipients
        
        Args:
            alerts_data: Dict with alert summary
            recipients: List of recipient emails
        
        Returns:
            Dict with results
        """
        
        subject = f"📊 Daily Health Check Report - {datetime.now().strftime('%Y-%m-%d')}"
        html = self._build_digest_html(alerts_data)
        
        results = {
            "total_recipients": len(recipients),
            "sent": 0,
            "failed": 0
        }
        
        for recipient in recipients:
            if self._send_email(recipient, subject, html):
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def send_incident_summary(self, incident_data: Dict, recipients: List[str]) -> bool:
        """
        Send incident summary email
        
        Args:
            incident_data: Incident details
            recipients: List of recipient emails
        
        Returns:
            True if all sent successfully
        """
        
        subject = f"🚨 Incident Summary: {incident_data.get('title', 'System Alert')}"
        html = self._build_incident_html(incident_data)
        
        success = True
        for recipient in recipients:
            if not self._send_email(recipient, subject, html):
                success = False
        
        return success
    
    def send_test_email(self, recipient: str) -> bool:
        """Send test email to verify configuration"""
        
        subject = "🤖 Alert Engine - Test Email"
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="background-color: white; padding: 20px; border-radius: 8px;">
                <h2>✅ Email Configuration Test</h2>
                <p>If you received this email, SendGrid is configured correctly!</p>
                <p><strong>Timestamp:</strong> {}</p>
                <p style="color: #666; font-size: 12px;">
                    Sent by Alert Engine
                </p>
            </div>
        </body>
        </html>
        """.format(datetime.now().isoformat())
        
        print(f"📨 Sending test email to {recipient}...")
        return self._send_email(recipient, subject, html)
    
    def _build_alert_html(self, alert: Dict) -> str:
        """Build HTML for alert email"""
        
        status_color = "#dc143c" if alert['status'] == 'failure' else "#ff8c00"
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                <h2 style="color: {status_color};">🚨 Alert Notification</h2>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid {status_color}; margin: 20px 0;">
                    <h3>{alert['activity_name']}</h3>
                    <p><strong>Status:</strong> <span style="color: {status_color};">{alert['status'].upper()}</span></p>
                    <p><strong>Response Code:</strong> {alert['response_code'] or 'N/A'}</p>
                    <p><strong>Response Time:</strong> {alert['response_time']:.2f}s</p>
                    <p><strong>URL:</strong> <a href="{alert['url']}">{alert['url']}</a></p>
                    <p><strong>Timestamp:</strong> {alert['timestamp']}</p>
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 4px; margin: 20px 0;">
                    <h4>Error Details:</h4>
                    <p><code>{alert['error_message'] or 'No error message'}</code></p>
                </div>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px;">
                    This is an automated alert from the Alert Engine.
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_digest_html(self, alerts_data: Dict) -> str:
        """Build HTML for daily digest email"""
        
        total = alerts_data.get('total_alerts', 0)
        actionable = alerts_data.get('actionable_alerts', 0)
        suppressed = alerts_data.get('suppressed_alerts', 0)
        test_defects = alerts_data.get('test_defects', 0)
        
        # Status indicator
        if actionable > 5:
            status_color = "#dc143c"
            status_text = "⚠️ Multiple Issues"
        elif actionable > 0:
            status_color = "#ff8c00"
            status_text = "⚠️ Issues Found"
        else:
            status_color = "#36a64f"
            status_text = "✅ All Clear"
        
        # Build activity table
        activities_html = ""
        if 'activities' in alerts_data:
            for activity in alerts_data['activities']:
                activities_html += f"""
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{activity.get('name', 'N/A')}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: center;">{activity.get('checks', 0)}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: center;">{activity.get('success_rate', 0)}%</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{activity.get('status', 'Unknown')}</td>
                </tr>
                """
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                <h1 style="color: #333; border-bottom: 3px solid {status_color}; padding-bottom: 10px;">
                    📊 Daily Health Check Report
                </h1>
                
                <div style="background-color: {status_color}20; padding: 15px; border-left: 4px solid {status_color}; margin: 20px 0; border-radius: 4px;">
                    <h2 style="color: {status_color}; margin: 0;">{status_text}</h2>
                    <p style="margin: 5px 0;">Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0;">
                    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 4px; text-align: center;">
                        <h3 style="margin: 0; color: #666; font-size: 14px;">Total Alerts</h3>
                        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #333;">{total}</p>
                    </div>
                    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 4px; text-align: center;">
                        <h3 style="margin: 0; color: #666; font-size: 14px;">Actionable</h3>
                        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #dc143c;">{actionable}</p>
                    </div>
                    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 4px; text-align: center;">
                        <h3 style="margin: 0; color: #666; font-size: 14px;">Suppressed</h3>
                        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #36a64f;">{suppressed}</p>
                    </div>
                </div>
                
                <h3 style="margin-top: 30px; color: #333;">Activity Status</h3>
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                    <thead>
                        <tr style="background-color: #f0f0f0;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Activity</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd;">Checks</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd;">Success Rate</th>
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {activities_html}
                    </tbody>
                </table>
                
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 4px; margin-top: 20px;">
                    <p style="margin: 0; color: #1976d2;">
                        <strong>Test Defects:</strong> {test_defects} simulated failures were injected for system testing.
                    </p>
                </div>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
                    This is an automated report from the Alert Engine.<br>
                    To manage your alert preferences, contact the DevOps team.
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_incident_html(self, incident_data: Dict) -> str:
        """Build HTML for incident email"""
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <div style="max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                <h1 style="color: #dc143c; border-bottom: 3px solid #dc143c; padding-bottom: 10px;">
                    🚨 Incident Alert
                </h1>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #dc143c; margin: 20px 0;">
                    <h2>{incident_data.get('title', 'System Incident')}</h2>
                    <p><strong>Severity:</strong> {incident_data.get('severity', 'Unknown')}</p>
                    <p><strong>Services Affected:</strong> {', '.join(incident_data.get('affected_services', []))}</p>
                    <p><strong>Time:</strong> {datetime.now().isoformat()}</p>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3>Description:</h3>
                    <p>{incident_data.get('description', 'No description provided')}</p>
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 4px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Actions Required:</h3>
                    <ul>
                        <li>Investigate the incident immediately</li>
                        <li>Check system logs and metrics</li>
                        <li>Update the incident ticket with findings</li>
                        <li>Notify relevant teams if escalation needed</li>
                    </ul>
                </div>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px;">
                    Alert Engine - Automated Incident Notification
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """
        Send email via Gmail SMTP
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: Email body (HTML)
        
        Returns:
            True if sent successfully
        """
        
        if self.dry_run:
            print(f"\n📋 [DRY-RUN] Would send email:")
            print(f"   To: {to_email}")
            print(f"   Subject: {subject}")
            self.sent_emails.append({
                "to": to_email,
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
                "status": "dry-run"
            })
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.email_user
            message["To"] = to_email
            
            # Attach HTML content
            part = MIMEText(html_content, "html")
            message.attach(part)
            
            # Send via Gmail SMTP
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.email_user, self.email_password)
                server.sendmail(self.email_user, to_email, message.as_string())
            
            self.sent_emails.append({
                "to": to_email,
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
                "status": "sent"
            })
            print(f"✓ Email sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"✗ Error sending email: {e}")
            self.sent_emails.append({
                "to": to_email,
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e)
            })
            return False
    
    def get_email_summary(self) -> Dict:
        """Get summary of sent emails"""
        
        return {
            "total_sent": len([e for e in self.sent_emails if e['status'] == 'sent']),
            "total_attempted": len(self.sent_emails),
            "emails": self.sent_emails
        }
