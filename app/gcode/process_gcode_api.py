from fastapi import APIRouter, Request
from app.core.request_helpers import get_param, require_params

router = APIRouter()

@router.post("/process")
async def process_gcode(request: Request):
    gcode_path = await get_param(request, "gcode_path")

    require_params({
        "gcode_path": gcode_path
    })

    # Placeholder for future processing logic
    return {
        "status": "success",
        "message": "G-code processed successfully"
    }
