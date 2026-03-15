from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user, get_current_admin
from ..models import Task, Payment, Project, User
from sqlalchemy import func

router = APIRouter(prefix="/admin")

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Basic Counts
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "paid").count()
    pending_payments = db.query(Task).filter(Task.status == "submitted").count()

    # User Counts
    total_buyers = db.query(User).filter(User.role == "buyer").count()
    total_developers = db.query(User).filter(User.role == "developer").count()

    # Financials (Your existing correct logic)
    total_revenue = db.query(
        func.sum(Task.hourly_rate * Task.hours_spent)
    ).filter(Task.status == "paid").scalar() or 0

    potential_revenue = db.query(
        func.sum(Task.hourly_rate * Task.hours_spent)
    ).filter(Task.status == "submitted").scalar() or 0

    total_hours = db.query(
        func.sum(Task.hours_spent)
    ).filter(Task.status.in_(["submitted", "paid"])).scalar() or 0

    return {
        "summary": {
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_payments": pending_payments,
        },
        "users": {
            "total_buyers": total_buyers,
            "total_developers": total_developers,
        },
        "financials": {
            "total_payments_received": completed_tasks, # Same as paid tasks
            "total_revenue": round(total_revenue, 2),
            "total_logged_hours": round(total_hours, 1),
            "potential_total_revenue": round(potential_revenue, 2)
        }
    }
@router.get("/all-users")
def get_all_users(db:Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(User).all()
    elif current_user.role == "buyer":
        # Buyers only need to see developers to assign tasks
        return db.query(User).filter(User.role == "developer").all()
    else:
        raise HTTPException(status_code=403, detail="Access denied")