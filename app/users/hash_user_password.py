from app.core.security_utils import hash_password

def generate_hashed_password(plain_password: str) -> str:
    """
    Use this only for migration or admin scripts.
    """
    return hash_password(plain_password)
