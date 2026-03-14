from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user, get_current_buyer, get_current_developer
from ..models import Task, User, Project
from ..schemas import TaskCreate
import shutil
import os

router = APIRouter(prefix="/tasks")

@router.post("/")
def create_task(task:TaskCreate, project_id:int, db:Session=Depends(get_db), current_user: User=Depends(get_current_buyer)):
    # Verify project belongs to this buyer
    project = db.query(Project).filter(Project.id == project_id, Project.buyer_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=project_id,
        developer_id=task.developer_id,
        hourly_rate=task.hourly_rate,
        status="todo"
    )
    db.add(new_task)
    db.commit()
    return {"message":"task created"}

@router.get("/my-tasks")
def get_developer_tasks(db:Session=Depends(get_db), current_user: User=Depends(get_current_developer)):
    # Tasks assigned to this developer
    return db.query(Task).filter(Task.developer_id == current_user.id).all()

@router.get("/project/{project_id}")
def get_project_tasks(project_id:int, db:Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    # Verify user has access to this project (Buyer or Assigned Developer)
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if current_user.role == "buyer" and project.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
        
    return db.query(Task).filter(Task.project_id == project_id).all()

@router.post("/{task_id}/submit")
def submit_task(
        task_id:int,
        hours:float,
        file:UploadFile=File(...),
        db:Session=Depends(get_db),
        current_user: User=Depends(get_current_developer)
):
    task = db.query(Task).filter(Task.id == task_id, Task.developer_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not assigned to you")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    path = f"uploads/{task_id}_{file.filename}"
    with open(path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    task.hours_spent = hours
    task.solution_zip = path
    task.status = "submitted"
    db.commit()
    return {"message":"task submitted"}

@router.get("/{task_id}/download")
def download_solution(task_id:int, db:Session=Depends(get_db), current_user: User=Depends(get_current_buyer)):
    task = db.query(Task).join(Project).filter(Task.id == task_id, Project.buyer_id == current_user.id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != "paid":
        raise HTTPException(status_code=403, detail="Access locked. Payment required to download solution")

    if not task.solution_zip or not os.path.exists(task.solution_zip):
        raise HTTPException(status_code=404, detail="Solution file not found")

    return FileResponse(path=task.solution_zip, filename=f"solution_{task_id}.zip")