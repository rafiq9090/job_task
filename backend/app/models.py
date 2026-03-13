from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    buyer_id = Column(Integer, ForeignKey("users.id"))

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    project_id = Column(Integer, ForeignKey("projects.id"))
    developer_id = Column(Integer, ForeignKey("users.id"))

    hourly_rate = Column(Float)
    hours_spent = Column(Float)

    status = Column(String, default="todo")

    solution_zip = Column(String)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer, ForeignKey("tasks.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))

    amount = Column(Float)
    status = Column(String)
