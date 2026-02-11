from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params
from app.core.security_utils import hash_password

router = APIRouter()

@router.post("/reset-password")
async def reset_password(request: Request):
    email = await get_param(request, "email")
    token = await get_param(request, "token")
    new_password = await get_param(request, "new_password")
    
    # We require either token or token+email
    require_params({
        "token": token,
        "new_password": new_password
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Use email if provided for extra security
        if email:
            cursor.execute(
                "SELECT id FROM users WHERE reset_token=%s AND email=%s",
                (token, email)
            )
        else:
            cursor.execute(
                "SELECT id FROM users WHERE reset_token=%s",
                (token,)
            )
        user = cursor.fetchone()

        if not user:
            return {
                "status": "error",
                "message": "Invalid or expired token"
            }

        hashed_password = hash_password(new_password)

        cursor.execute(
            "UPDATE users SET password=%s, reset_token=NULL WHERE id=%s",
            (hashed_password, user["id"])
        )
        conn.commit()

        # Get updated user data for auto-login
        cursor.execute("SELECT id, name, email FROM users WHERE id=%s", (user["id"],))
        updated_user = cursor.fetchone()

        return {
            "status": "success",
            "message": "Password reset successfully",
            "data": updated_user
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Server error: {str(e)}"
        }
    finally:
        cursor.close()
        conn.close()
