from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/profile/update")
async def update_profile(request: Request):
    user_id = await get_param(request, "user_id")
    name = await get_param(request, "name")
    email = await get_param(request, "email")

    require_params({
        "user_id": user_id,
        "name": name,
        "email": email
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, user_id)
    )

    return {
        "status": "success",
        "message": "Profile updated successfully"
    }
