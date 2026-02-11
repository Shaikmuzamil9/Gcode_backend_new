from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params
from app.core.security_utils import verify_password

router = APIRouter()

@router.post("/login")
async def login(request: Request):
    email = await get_param(request, "email")
    password = await get_param(request, "password")

    require_params({
        "email": email,
        "password": password
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(
        "SELECT id, name, email, password FROM users WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user or not verify_password(password, user["password"]):
        return {
            "status": "error",
            "message": "Invalid email or password"
        }

    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "id": user["id"],
            "name": user.get("name", ""),
            "email": user.get("email", "")
        }
    }
