from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/delete")
async def delete_device(request: Request):
    device_id = await get_param(request, "device_id")

    require_params({
        "device_id": device_id
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM devices WHERE device_id=%s",
        (device_id,)
    )

    if cursor.rowcount == 0:
        return {
            "status": "error",
            "message": "Device not found"
        }

    return {
        "status": "success",
        "message": "Device deleted successfully"
    }
