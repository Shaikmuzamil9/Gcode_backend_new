from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params
from app.core.security_utils import generate_token
from app.core.otp_utils import OTPService
from app.core.email_utils import EmailService

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(request: Request):
    email = await get_param(request, "email")

    require_params({
        "email": email
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT id, name FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()

        if not user:
            return {
                "status": "error",
                "message": "Email not found"
            }

        # Generate and Store OTP
        otp_service = OTPService()
        email_service = EmailService()
        
        otp = otp_service.generate_otp()
        
        if not otp_service.store_otp(email, otp):
            return {
                "status": "error",
                "message": "Failed to generate OTP"
            }

        # Also store in users table for reset-password compatibility
        cursor.execute(
            "UPDATE users SET reset_token=%s WHERE email=%s",
            (otp, email)
        )
        conn.commit()

        # Send OTP Email
        user_name = user.get("name", "User")
        if not email_service.send_otp_email(email, otp, user_name):
            return {
                "status": "error",
                "message": "Failed to send OTP to email. Check server logs."
            }

        return {
            "status": "success",
            "message": "OTP sent successfully to your email"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Server error: {str(e)}"
        }
    finally:
        cursor.close()
        conn.close()
