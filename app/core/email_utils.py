import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import pathlib

# Load .env from project root
env_path = pathlib.Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class EmailService:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_ADDRESS")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        # Debug: Print if variables are loaded
        if not self.sender_email or not self.sender_password:
            print(f"⚠️ WARNING: Email credentials not loaded! EMAIL: {self.sender_email}")
    
    def send_otp_email(self, recipient_email: str, otp_code: str, user_name: str = "User"):
        """Send OTP to user's email"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Your OTP Verification Code"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # HTML email body
            html = f"""\
            <html>
              <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                  <h2 style="color: #333;">Hello {user_name},</h2>
                  <p style="font-size: 16px; color: #555;">
                    Your One-Time Password (OTP) for verification is:
                  </p>
                  <div style="background-color: #f0f0f0; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                    <h1 style="color: #007bff; margin: 0; letter-spacing: 5px;">{otp_code}</h1>
                  </div>
                  <p style="font-size: 14px; color: #888;">
                    ⚠️ This OTP will expire in 10 minutes.
                  </p>
                  <p style="font-size: 14px; color: #888;">
                    If you didn't request this OTP, please ignore this email.
                  </p>
                  <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                  <p style="font-size: 12px; color: #999;">
                    This is an automated message. Please do not reply to this email.
                  </p>
                </div>
              </body>
            </html>
            """
            
            part = MIMEText(html, "html")
            message.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            print(f"✅ OTP email sent successfully to {recipient_email}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Email authentication failed: {str(e)}")
            print("Check your EMAIL_ADDRESS and EMAIL_PASSWORD in .env file")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
    
    def send_welcome_email(self, recipient_email: str, user_name: str):
        """Send welcome email to new user"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Welcome to GCODE API!"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            html = f"""\
            <html>
              <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                  <h2 style="color: #333;">Welcome {user_name}! 🎉</h2>
                  <p style="font-size: 16px; color: #555;">
                    Thank you for registering with GCODE API. Your account has been created successfully.
                  </p>
                  <p style="font-size: 14px; color: #888;">
                    You can now log in and start using our services.
                  </p>
                  <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                  <p style="font-size: 12px; color: #999;">
                    If you have any questions, please contact our support team.
                  </p>
                </div>
              </body>
            </html>
            """
            
            part = MIMEText(html, "html")
            message.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            print(f"✅ Welcome email sent to {recipient_email}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Email authentication failed: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
