from fastapi import APIRouter, Request
from app.core.request_helpers import get_param, require_params
from app.core.otp_utils import OTPService
from app.core.email_utils import EmailService
from app.core.db_connection import get_db_connection

router = APIRouter()
email_service = EmailService()
otp_service = OTPService()


@router.post("/request-otp")
async def request_otp(request: Request):
    """Request OTP for email verification"""
    try:
        email = await get_param(request, "email")
        
        require_params({
            "email": email
        })
        
        # Check if email exists in users table
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, name FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            
            if not user:
                return {
                    "status": "error",
                    "message": "Email not found in our system"
                }
            
            # Generate OTP
            otp = otp_service.generate_otp()
            
            # Store OTP in database
            if not otp_service.store_otp(email, otp):
                return {
                    "status": "error",
                    "message": "Failed to generate OTP. Please try again."
                }
            
            # Send OTP to email
            if not email_service.send_otp_email(email, otp, user.get("name", "User")):
                return {
                    "status": "error",
                    "message": "Failed to send OTP to email. Please check email configuration."
                }
            
            return {
                "status": "success",
                "message": "OTP sent successfully to your email",
                "data": {
                    "email": email,
                    "otp_expiry_minutes": OTPService.OTP_EXPIRY_MINUTES
                }
            }
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error requesting OTP: {str(e)}"
        }


@router.post("/verify-otp")
async def verify_otp(request: Request):
    """Verify OTP code"""
    try:
        email = await get_param(request, "email")
        otp_code = await get_param(request, "otp_code")
        
        # Fallback to 'otp' parameter name for Android app compatibility
        if otp_code is None:
            otp_code = await get_param(request, "otp")
        
        require_params({
            "email": email,
            "otp_code": otp_code
        })
        
        # Verify OTP
        result = otp_service.verify_otp(email, otp_code)
        
        if not result["valid"]:
            return {
                "status": "error",
                "message": result["message"]
            }
        
        # Delete OTP after successful verification
        otp_service.delete_otp(email)
        
        # Get user details
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, name, email FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            
            if not user:
                return {
                    "status": "error",
                    "message": "User not found"
                }
            
            return {
                "status": "success",
                "message": "OTP verified successfully",
                "data": {
                    "id": user["id"],
                    "name": user.get("name", ""),
                    "email": user.get("email", "")
                }
            }
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error verifying OTP: {str(e)}"
        }


@router.post("/resend-otp")
async def resend_otp(request: Request):
    """Resend OTP to email"""
    try:
        email = await get_param(request, "email")
        
        require_params({
            "email": email
        })
        
        # Check if email exists
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, name FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            
            if not user:
                return {
                    "status": "error",
                    "message": "Email not found in our system"
                }
            
            # Generate new OTP
            otp = otp_service.generate_otp()
            
            # Store OTP
            if not otp_service.store_otp(email, otp):
                return {
                    "status": "error",
                    "message": "Failed to generate OTP"
                }
            
            # Send OTP
            if not email_service.send_otp_email(email, otp, user.get("name", "User")):
                return {
                    "status": "error",
                    "message": "Failed to send OTP to email"
                }
            
            return {
                "status": "success",
                "message": "OTP resent successfully to your email",
                "data": {
                    "email": email,
                    "otp_expiry_minutes": OTPService.OTP_EXPIRY_MINUTES
                }
            }
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error resending OTP: {str(e)}"
        }


@router.get("/otp-status/{email}")
async def get_otp_status(email: str):
    """Get OTP status for email"""
    try:
        status = otp_service.get_otp_status(email)
        
        if not status["exists"]:
            return {
                "status": "error",
                "message": status["message"]
            }
        
        return {
            "status": "success",
            "data": status
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error getting OTP status: {str(e)}"
        }
