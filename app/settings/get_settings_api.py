from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.get("/get")
async def get_settings(request: Request):
    user_id = await get_param(request, "user_id")

    require_params({
        "user_id": user_id
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT setting_key, setting_value
        FROM settings
        WHERE user_id=%s
        """,
        (user_id,)
    )

    settings = {row["setting_key"]: row["setting_value"] for row in cursor.fetchall()}

    return {
        "status": "success",
        "settings": settings
    }
