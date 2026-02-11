from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/add")
async def add_activity_log(request: Request):
    user_id = await get_param(request, "user_id")
    action = await get_param(request, "action")

    require_params({
        "user_id": user_id,
        "action": action
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO activity_logs (user_id, action)
        VALUES (%s, %s)
        """,
        (user_id, action)
    )

    return {
        "status": "success",
        "message": "Activity logged"
    }
