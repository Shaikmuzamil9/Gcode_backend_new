from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/save")
async def save_gcode(request: Request):
    user_id = await get_param(request, "user_id")
    name = await get_param(request, "name")
    gcode_path = await get_param(request, "gcode_path")

    require_params({
        "user_id": user_id,
        "name": name,
        "gcode_path": gcode_path
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO gcodes (user_id, name, gcode_path)
        VALUES (%s, %s, %s)
        """,
        (user_id, name, gcode_path)
    )

    return {
        "status": "success",
        "message": "G-code saved successfully"
    }
