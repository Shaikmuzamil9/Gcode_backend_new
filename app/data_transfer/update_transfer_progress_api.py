from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/progress")
async def update_transfer_progress(request: Request):
    transfer_id = await get_param(request, "transfer_id")
    progress = await get_param(request, "progress")
    status = await get_param(request, "status")

    require_params({
        "transfer_id": transfer_id,
        "progress": progress,
        "status": status
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE data_transfers
        SET progress=%s, status=%s
        WHERE id=%s
        """,
        (progress, status, transfer_id)
    )

    return {
        "status": "success",
        "message": "Transfer progress updated"
    }
