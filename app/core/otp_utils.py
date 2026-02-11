import random
import string
from datetime import datetime, timedelta
from app.core.db_connection import get_db_connection

class OTPService:
    OTP_LENGTH = 4
    OTP_EXPIRY_MINUTES = 10
    
    @staticmethod
    def generate_otp(length: int = OTP_LENGTH) -> str:
        """Generate a random OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def store_otp(email: str, otp: str) -> bool:
        """Store OTP in database with expiry"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Calculate expiry time
            expiry_time = datetime.now() + timedelta(minutes=OTPService.OTP_EXPIRY_MINUTES)
            
            # Delete any existing OTP for this email
            cursor.execute("DELETE FROM otps WHERE email=%s", (email,))
            
            # Insert new OTP
            cursor.execute(
                "INSERT INTO otps (email, otp_code, expiry_time, created_at) VALUES (%s, %s, %s, NOW())",
                (email, otp, expiry_time)
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing OTP: {str(e)}")
            return False
    
    @staticmethod
    def verify_otp(email: str, otp: str) -> dict:
        """Verify OTP for given email"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get OTP from database
            cursor.execute(
                "SELECT * FROM otps WHERE email=%s AND otp_code=%s ORDER BY created_at DESC LIMIT 1",
                (email, otp)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not result:
                return {"valid": False, "message": "Invalid OTP"}
            
            # Check if OTP has expired
            expiry_time = result['expiry_time']
            if datetime.now() > expiry_time:
                return {"valid": False, "message": "OTP has expired"}
            
            return {"valid": True, "message": "OTP verified successfully"}
        except Exception as e:
            print(f"Error verifying OTP: {str(e)}")
            return {"valid": False, "message": "Error verifying OTP"}
    
    @staticmethod
    def delete_otp(email: str) -> bool:
        """Delete OTP after successful verification"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM otps WHERE email=%s", (email,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting OTP: {str(e)}")
            return False
    
    @staticmethod
    def get_otp_status(email: str) -> dict:
        """Get OTP status for email"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM otps WHERE email=%s ORDER BY created_at DESC LIMIT 1",
                (email,)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not result:
                return {"exists": False, "message": "No OTP found"}
            
            # Check if OTP has expired
            expiry_time = result['expiry_time']
            if datetime.now() > expiry_time:
                return {"exists": False, "message": "OTP has expired"}
            
            # Calculate remaining time
            remaining_seconds = (expiry_time - datetime.now()).total_seconds()
            
            return {
                "exists": True,
                "email": email,
                "created_at": result['created_at'],
                "expiry_time": expiry_time,
                "remaining_seconds": int(remaining_seconds)
            }
        except Exception as e:
            print(f"Error getting OTP status: {str(e)}")
            return {"exists": False, "message": "Error getting OTP status"}
