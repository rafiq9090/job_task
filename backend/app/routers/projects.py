from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_buyer
from ..models import Project, User
from ..schemas import ProjectCreate

router = APIRouter(prefix="/projects")

@router.post("/")
def create_project(project:ProjectCreate, db:Session=Depends(get_db), current_user: User=Depends(get_current_buyer)):
    new_project = Project(
        title=project.title,
        buyer_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    return {"message":"project created"}

@router.get("/")
def get_my_projects(db:Session=Depends(get_db), current_user: User=Depends(get_current_buyer)):
    projects = db.query(Project).filter(Project.buyer_id == current_user.id).all()
    return projects