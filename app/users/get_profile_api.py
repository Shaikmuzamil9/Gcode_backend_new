from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.get("/profile")
async def get_profile(request: Request):
    user_id = await get_param(request, "user_id")

    require_params({
        "user_id": user_id
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name, email, created_at FROM users WHERE id=%s",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        return {
            "status": "error",
            "message": "User not found"
        }

    return {
        "status": "success",
        "user": user
    }
