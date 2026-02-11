from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/register")
async def register_device(request: Request):
    user_id = await get_param(request, "user_id")
    device_name = await get_param(request, "device_name")
    device_id = await get_param(request, "device_id")

    require_params({
        "user_id": user_id,
        "device_name": device_name,
        "device_id": device_id
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if device already exists
    cursor.execute(
        "SELECT id FROM devices WHERE device_id=%s",
        (device_id,)
    )
    if cursor.fetchone():
        return {
            "status": "error",
            "message": "Device already registered"
        }

    cursor.execute(
        """
        INSERT INTO devices (user_id, device_name, device_id)
        VALUES (%s, %s, %s)
        """,
        (user_id, device_name, device_id)
    )

    return {
        "status": "success",
        "message": "Device registered successfully"
    }
