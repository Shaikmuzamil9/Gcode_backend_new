import html
from fastapi import Request, HTTPException

def clean_input(value):
    if isinstance(value, dict):
        return value
    if value is None:
        return None
    return html.escape(str(value).strip())

async def get_param(request: Request, key: str):
    # JSON body
    if request.headers.get("content-type", "").startswith("application/json"):
        body = await request.json()
        if key in body:
            return clean_input(body.get(key))

    # Form data
    form = await request.form()
    if key in form:
        return clean_input(form.get(key))

    # Query params
    if key in request.query_params:
        return clean_input(request.query_params.get(key))

    return None

def require_params(params: dict):
    for name, value in params.items():
        if value in (None, ""):
            raise HTTPException(
                status_code=400,
                detail=f"{name} is required"
            )
