from pydantic import BaseModel

class UserCreate(BaseModel):
    name:str
    email:str
    password:str
    role:str

class ProjectCreate(BaseModel):
    title:str

class TaskCreate(BaseModel):
    title:str
    description:str
    developer_id:int
    hourly_rate:float
