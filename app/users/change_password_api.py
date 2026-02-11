from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params
from app.core.security_utils import hash_password, verify_password

router = APIRouter()

@router.post("/password/change")
async def change_password(request: Request):
    user_id = await get_param(request, "user_id")
    old_password = await get_param(request, "old_password")
    new_password = await get_param(request, "new_password")

    require_params({
        "user_id": user_id,
        "old_password": old_password,
        "new_password": new_password
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT password FROM users WHERE id=%s",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user or not verify_password(old_password, user["password"]):
        return {
            "status": "error",
            "message": "Old password is incorrect"
        }

    hashed_password = hash_password(new_password)

    cursor.execute(
        "UPDATE users SET password=%s WHERE id=%s",
        (hashed_password, user_id)
    )

    return {
        "status": "success",
        "message": "Password changed successfully"
    }
