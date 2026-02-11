from fastapi import APIRouter, Request
from app.core.db_connection import get_db_connection
from app.core.request_helpers import get_param, require_params
from app.core.security_utils import hash_password

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    name = await get_param(request, "name")
    email = await get_param(request, "email")
    password = await get_param(request, "password")

    require_params({
        "name": name,
        "email": email,
        "password": password
    })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM users WHERE email=%s",
        (email,)
    )
    if cursor.fetchone():
        return {
            "status": "error",
            "message": "Email already exists"
        }

    hashed_password = hash_password(password)

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hashed_password)
    )
    conn.commit()
    
    # Get the newly created user ID
    user_id = cursor.lastrowid
    
    # Fallback if lastrowid is not reliable
    if not user_id:
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        result = cursor.fetchone()
        if result:
            user_id = result['id']
    
    cursor.close()
    conn.close()

    return {
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "id": user_id,
            "name": name,
            "email": email
        }
    }
