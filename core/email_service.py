"""
Email Service for Patient Notifications
Sends prediction reports and appointment notifications via email
"""
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Optional
import os
from pathlib import Path

class EmailService:
    """
    Email service for sending notifications to patients
    """
    
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', 'cancercare.lab@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.sender_name = os.getenv('SENDER_NAME', 'CancerCare Lab')
        
        # Email queue for async sending
        self.email_queue = []
        self.lock = threading.Lock()
        
        # Statistics
        self.emails_sent = 0
        self.emails_failed = 0
    
    def send_email(self, to_email: str, subject: str, html_body: str, text_body: str = None) -> bool:
        """
        Send email to recipient
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if text_body:
                part1 = MIMEText(text_body, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                
                # Only try to login if password is provided
                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                
                server.send_message(msg)
            
            with self.lock:
                self.emails_sent += 1
            
            print(f" Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            with self.lock:
                self.emails_failed += 1
            print(f" Email failed to {to_email}: {e}")
            return False
    
    def send_email_async(self, to_email: str, subject: str, html_body: str, text_body: str = None):
        """
        Send email asynchronously in background thread
        """
        thread = threading.Thread(
            target=self.send_email,
            args=(to_email, subject, html_body, text_body),
            daemon=True
        )
        thread.start()
    
    def send_prediction_report(self, patient_email: str, patient_name: str, risk_level: str, confidence: float, recommendations: str) -> bool:
        """
        Send prediction report email to patient
        """
        subject = f"CancerCare Lab - Your Risk Assessment Report"
        
        # HTML email template
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #00d9ff 0%, #0088cc 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f5f5f5;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .risk-box {{
                    background: {'#ff006e' if risk_level == 'High' else '#ffbe0b' if risk_level == 'Medium' else '#00ff88'};
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 10px;
                    margin: 20px 0;
                    font-size: 24px;
                    font-weight: bold;
                }}
                .info-box {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 4px solid #00d9ff;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #ddd;
                    color: #666;
                    font-size: 12px;
                }}
                .button {{
                    display: inline-block;
                    background: #00d9ff;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1> CancerCare Lab</h1>
                <p>Risk Assessment Report</p>
            </div>
            <div class="content">
                <h2>Dear {patient_name},</h2>
                <p>Your lung cancer risk assessment has been completed. Please review the details below:</p>
                
                <div class="risk-box">
                     {risk_level.upper()} RISK
                    <br>
                    <span style="font-size: 16px;">Confidence: {confidence:.1%}</span>
                </div>
                
                <div class="info-box">
                    <h3> Recommendations</h3>
                    <p>{recommendations}</p>
                </div>
                
                <div class="info-box">
                    <h3> Next Steps</h3>
                    <p>
                        {'<strong>URGENT:</strong> Please schedule an immediate consultation with an oncologist.' if risk_level == 'High' else 
                         'We recommend scheduling a follow-up appointment within 3-6 months.' if risk_level == 'Medium' else
                         'Continue with regular health check-ups and maintain a healthy lifestyle.'}
                    </p>
                </div>
                
                <p style="text-align: center;">
                    <a href="http://localhost:8501" class="button">View Full Report</a>
                </p>
                
                <div class="footer">
                    <p><strong>CancerCare Lab</strong></p>
                    <p>Advanced AI-Powered Cancer Risk Analysis</p>
                    <p>Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p style="font-size: 10px; margin-top: 10px;">
                        This is an automated report. Please do not reply to this email.<br>
                        For questions, contact your healthcare provider.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_body = f"""
        CancerCare Lab - Risk Assessment Report
        
        Dear {patient_name},
        
        Your lung cancer risk assessment has been completed.
        
        Result: {risk_level.upper()} RISK
        Confidence: {confidence:.1%}
        
        Recommendations:
        {recommendations}
        
        Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        CancerCare Lab
        """
        
        return self.send_email_async(patient_email, subject, html_body, text_body)
    
    def send_appointment_notification(self, patient_email: str, patient_name: str, doctor_name: str, appointment_date: str, reason: str = "") -> bool:
        """
        Send appointment notification email to patient
        """
        subject = f"CancerCare Lab - Appointment Scheduled with {doctor_name}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #00d9ff 0%, #0088cc 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f5f5f5;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .appointment-box {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 4px solid #00d9ff;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #ddd;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1> Appointment Scheduled</h1>
            </div>
            <div class="content">
                <h2>Dear {patient_name},</h2>
                <p>Your appointment has been successfully scheduled.</p>
                
                <div class="appointment-box">
                    <h3>Appointment Details:</h3>
                    <p><strong>Doctor:</strong> {doctor_name}</p>
                    <p><strong>Date & Time:</strong> {appointment_date}</p>
                    {f'<p><strong>Reason:</strong> {reason}</p>' if reason else ''}
                </div>
                
                <div class="appointment-box">
                    <h3> Location</h3>
                    <p>CancerCare Lab<br>Main Medical Center</p>
                </div>
                
                <div class="appointment-box">
                    <h3>ℹ Important Notes</h3>
                    <ul>
                        <li>Please arrive 15 minutes before your appointment</li>
                        <li>Bring your medical records and ID</li>
                        <li>If you need to reschedule, contact us at least 24 hours in advance</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p><strong>CancerCare Lab</strong></p>
                    <p>Email Sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        CancerCare Lab - Appointment Scheduled
        
        Dear {patient_name},
        
        Your appointment has been successfully scheduled.
        
        Doctor: {doctor_name}
        Date & Time: {appointment_date}
        {f'Reason: {reason}' if reason else ''}
        
        Please arrive 15 minutes before your appointment.
        
        CancerCare Lab
        """
        
        return self.send_email_async(patient_email, subject, html_body, text_body)
    
    def get_statistics(self):
        """Get email statistics"""
        return {
            'emails_sent': self.emails_sent,
            'emails_failed': self.emails_failed,
            'success_rate': round(self.emails_sent / (self.emails_sent + self.emails_failed) * 100, 2) if (self.emails_sent + self.emails_failed) > 0 else 0
        }

# Global email service instance
email_service = EmailService()
