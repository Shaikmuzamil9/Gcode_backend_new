from fastapi import APIRouter, UploadFile, File, Form
from app.core.db_connection import get_db_connection
import os
import uuid

router = APIRouter()

# Absolute directory on disk
UPLOAD_DIR = os.path.join("app", "uploads", "images")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_image(
    user_id: int = Form(...),
    image: UploadFile = File(...)
):
    # Generate safe unique filename
    filename = f"{uuid.uuid4()}_{image.filename}"

    # Full file system path (used internally & stored in DB)
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file to disk
    with open(file_path, "wb") as f:
        f.write(await image.read())

    # Save INTERNAL path in database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO images (user_id, image_path) VALUES (%s, %s)",
        (user_id, file_path)
    )
    conn.commit()

    # PUBLIC path for frontend (URL-friendly)
    public_path = f"/uploads/images/{filename}"
    public_url = f"http://180.235.121.253:8030{public_path}"

    return {
        "status": "success",
        "image_path": public_path,
        "image_url": public_url
    }
