from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib

SECRET_KEY = "autoagent-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

USERS_DB = {
    "pushpraj": {
        "username": "pushpraj",
        "full_name": "Pushpraj Singh",
        "hashed_password": hash_password("admin123"),
        "role": "admin"
    },
    "demo": {
        "username": "demo",
        "full_name": "Demo User",
        "hashed_password": hash_password("demo123"),
        "role": "user"
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def get_user(username: str):
    if username in USERS_DB:
        return USERS_DB[username]
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None