from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:str

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