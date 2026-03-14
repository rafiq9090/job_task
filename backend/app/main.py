from fastapi import FastAPI
from .database import Base,engine

from .routers import users,projects,tasks,payment,admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(payment.router)
app.include_router(admin.router)