from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.get("/list")
async def list_devices(request: Request):
    user_id = await get_param(request, "user_id")

    require_params({
        "user_id": user_id
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, device_name, device_id, created_at
        FROM devices
        WHERE user_id=%s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    devices = cursor.fetchall()

    return {
        "status": "success",
        "devices": devices
    }
