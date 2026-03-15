import re
from pydantic import BaseModel,EmailStr,field_validator


class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Password must contain at least one special character')
        return v
    

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class ProjectCreate(BaseModel):
    title:str

class TaskCreate(BaseModel):
    title:str
    description:str
    developer_id:int
    hourly_rate:float
    project_id:int