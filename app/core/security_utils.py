import bcrypt
import secrets

def hash_password(password: str) -> str:
    # bcrypt max length = 72 bytes
    safe_password = password[:72].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(safe_password, salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    safe_password = password[:72].encode('utf-8')
    try:
        return bcrypt.checkpw(safe_password, hashed.encode('utf-8'))
    except Exception:
        return False

def generate_token() -> str:
    return secrets.token_hex(32)
