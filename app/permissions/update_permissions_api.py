from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/update")
async def update_permissions(request: Request):
    user_id = await get_param(request, "user_id")
    permissions = await get_param(request, "permissions")

    require_params({
        "user_id": user_id,
        "permissions": permissions
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM permissions WHERE user_id=%s",
        (user_id,)
    )

    for perm in permissions.split(","):
        cursor.execute(
            "INSERT INTO permissions (user_id, permission) VALUES (%s, %s)",
            (user_id, perm.strip())
        )

    return {
        "status": "success",
        "message": "Permissions updated"
    }
