from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/capture")
async def capture_image(request: Request):
    user_id = await get_param(request, "user_id")
    image_path = await get_param(request, "image_path")

    require_params({
        "user_id": user_id,
        "image_path": image_path
    })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO images (user_id, image_path)
        VALUES (%s, %s)
        """,
        (user_id, image_path)
    )

    return {
        "status": "success",
        "message": "Image captured successfully"
    }
