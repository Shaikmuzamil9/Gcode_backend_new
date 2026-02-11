from fastapi import APIRouter
from app.core.db_connection import get_db_connection

router = APIRouter()

@router.get("/get")
def get_permissions(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT upload_image, convert_gcode, transfer_gcode
        FROM permissions
        WHERE user_id = %s
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    if not row:
        return {"status": "success", "permissions": {}}

    return {
        "status": "success",
        "permissions": {
            "upload_image": bool(row["upload_image"]),
            "convert_gcode": bool(row["convert_gcode"]),
            "transfer_gcode": bool(row["transfer_gcode"])
        }
    }
