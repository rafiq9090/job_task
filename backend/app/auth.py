from jose import jwt 
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET = "secretkey"

pwd = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd.hash(password)

def verify_password(password, hashed):
    return pwd.verify(password, hashed)

def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(data, SECRET, algorithm="HS256")