from fastapi import APIRouter, Request, HTTPException
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/delete_account")
async def delete_account(request: Request):
    user_id = await get_param(request, "user_id")
    
    require_params({
        "user_id": user_id
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            return {
                "status": "error",
                "message": "User not found"
            }

        # Delete user
        # Note: If there are foreign key constraints, we might need to delete related data or handle them.
        # For now, we'll do a simple delete.
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()

        return {
            "status": "success",
            "message": "Account deleted successfully"
        }
    except Exception as e:
        conn.rollback()
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        cursor.close()
        conn.close()
