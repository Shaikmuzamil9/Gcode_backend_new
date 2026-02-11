from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.get("/get")
async def get_gcode(request: Request):
    gcode_id = await get_param(request, "gcode_id")

    require_params({
        "gcode_id": gcode_id
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM gcodes WHERE id=%s",
        (gcode_id,)
    )

    gcode = cursor.fetchone()

    if not gcode:
        return {
            "status": "error",
            "message": "G-code not found"
        }

    return {
        "status": "success",
        "gcode": gcode
    }
