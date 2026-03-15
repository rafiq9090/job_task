from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user, get_current_admin
from ..models import Task, Payment, Project, User
from sqlalchemy import func

router = APIRouter(prefix="/admin")

@router.get("/stats")
def get_dashboard_stats(db:Session=Depends(get_db), current_user: User=Depends(get_current_admin)):
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()
    
    # User Breakdown
    total_buyers = db.query(User).filter(User.role == "buyer").count()
    total_developers = db.query(User).filter(User.role == "developer").count()

    # Task Status Breakdown
    completed_tasks = db.query(Task).filter(Task.status=="paid").count()
    pending_payments = db.query(Task).filter(Task.status=="submitted").count()
    
    # Hours and Revenue
    total_hours = db.query(func.sum(Task.hours_spent)).scalar() or 0
    total_revenue = db.query(func.sum(Payment.amount)).scalar() or 0
    
    # Total payments count
    total_payments_count = db.query(Payment).count()

    # Budget/Revenue by Status (Hourly rate * Hours)
    total_billed = db.query(func.sum(Task.hourly_rate * Task.hours_spent)).scalar() or 0

    return {
        "summary": {
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_payments": pending_payments,
        },
        "users": {
            "total_buyers": total_buyers,
            "total_developers": total_developers
        },
        "financials": {
            "total_payments_received": total_payments_count,
            "total_revenue": total_revenue,
            "total_logged_hours": total_hours,
            "potential_total_revenue": total_billed
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