from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import traceback
from app.gcode.engine_v2 import generate_vector_gcode, generate_raster_gcode
from typing import Optional

router = APIRouter()


class ConvertRequest(BaseModel):
    image_path: str  # /uploads/images/xxx.jpg
    mode: Optional[str] = "vector"  # "vector" or "raster"


@router.post("/convert")
def convert(req: ConvertRequest):

    if not req.image_path.startswith("/uploads/"):
        raise HTTPException(status_code=400, detail="Invalid image path")

    # PUBLIC → DISK PATH
    disk_image_path = os.path.join("app", req.image_path.lstrip("/"))

    if not os.path.exists(disk_image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        mode = (req.mode or "vector").lower()
        if mode == "vector":
            gcode_disk_path = generate_vector_gcode(disk_image_path)
        elif mode == "raster":
            gcode_disk_path = generate_raster_gcode(disk_image_path)
        else:
            raise HTTPException(status_code=400, detail="mode must be 'vector' or 'raster'")

        # Normalize and return public path under /uploads
        normalized = gcode_disk_path.replace("\\", "/")
        uploads_index = normalized.find("/uploads/")
        if uploads_index == -1:
            raise HTTPException(status_code=500, detail="Invalid gcode path")

        gcode_public_path = normalized[uploads_index:]

        return {
            "status": "success",
            "gcode_path": gcode_public_path,
            "gcode_url": f"http://localhost:8000{gcode_public_path}"
        }
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating gcode: {str(e)}")



@router.get("/preview")
def preview(image_path: str = Query(..., description="Public image path starting with /uploads/")):
    """Return a small preview image path for the provided uploaded image.
    The endpoint returns a JSON with `preview_path` (under /uploads) that can be loaded directly.
    """
    if not image_path.startswith("/uploads/"):
        raise HTTPException(status_code=400, detail="Invalid image path")

    disk_image_path = os.path.join("app", image_path.lstrip("/"))
    if not os.path.exists(disk_image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        # create previews dir next to gcodes
        previews_dir = os.path.abspath(os.path.join(os.path.dirname(disk_image_path), "..", "gcodes", "previews"))
        os.makedirs(previews_dir, exist_ok=True)

        from PIL import Image
        im = Image.open(disk_image_path)
        im.thumbnail((400, 400))

        preview_name = f"{uuid.uuid4()}.jpg"
        preview_disk = os.path.join(previews_dir, preview_name)
        im.save(preview_disk, format="JPEG", quality=80)

        normalized = preview_disk.replace("\\", "/")
        uploads_index = normalized.find("/uploads/")
        if uploads_index == -1:
            # return absolute path fallback
            return {"status": "success", "preview_path": preview_disk}

        preview_public = normalized[uploads_index:]
        return {"status": "success", "preview_path": preview_public}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download")
def download(gcode_path: str = Query(..., description="Public gcode path starting with /uploads/")):
    """Download generated G-code file. Supply `gcode_path` as the public path returned earlier."""
    if not gcode_path.startswith("/uploads/"):
        raise HTTPException(status_code=400, detail="Invalid gcode path")

    disk_gcode = os.path.join("app", gcode_path.lstrip("/"))
    if not os.path.exists(disk_gcode):
        raise HTTPException(status_code=404, detail="G-code not found")

    return FileResponse(disk_gcode, media_type="text/plain", filename=os.path.basename(disk_gcode))
