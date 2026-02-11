from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/update")
async def update_settings(request: Request):
    user_id = await get_param(request, "user_id")
    settings = await get_param(request, "settings")

    require_params({
        "user_id": user_id,
        "settings": settings
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    for key, value in settings.items():
        cursor.execute(
            """
            INSERT INTO settings (user_id, setting_key, setting_value)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE setting_value=%s
            """,
            (user_id, key, value, value)
        )

    return {
        "status": "success",
        "message": "Settings updated successfully"
    }
