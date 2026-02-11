from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/start")
async def start_transfer(request: Request):
    user_id = await get_param(request, "user_id")
    device_id = await get_param(request, "device_id")
    gcode_id = await get_param(request, "gcode_id")

    require_params({
        "user_id": user_id,
        "device_id": device_id,
        "gcode_id": gcode_id
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO data_transfers (user_id, device_id, gcode_id, status)
        VALUES (%s, %s, %s, 'started')
        """,
        (user_id, device_id, gcode_id)
    )

    transfer_id = cursor.lastrowid

    return {
        "status": "success",
        "message": "Transfer started",
        "transfer_id": transfer_id
    }
