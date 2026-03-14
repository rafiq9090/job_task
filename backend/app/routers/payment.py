from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_buyer
from ..models import Payment, Task, Project, User

router = APIRouter(prefix="/payments")

@router.post("/{task_id}")
def pay_task(task_id:int, db:Session=Depends(get_db), current_user: User=Depends(get_current_buyer)):
    # Verify task belongs to a project owned by this buyer
    task = db.query(Task).join(Project).filter(Task.id == task_id, Project.buyer_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "submitted":
        raise HTTPException(status_code=400, detail=f"Task status is {task.status}. Only submitted tasks can be paid.")

    if not task.hours_spent:
         raise HTTPException(status_code=400, detail="Cannot pay for task with 0 hours logged")

    amount = task.hourly_rate * task.hours_spent

    payment = Payment(
        task_id=task_id,
        buyer_id=current_user.id,
        amount=amount,
        status="paid"
    )

    task.status="paid"

    db.add(payment)
    db.commit()

    return {"message":"payment success", "amount_paid": amount}

@router.get("/")
def get_my_payments(db:Session=Depends(get_db), current_user: User=Depends(get_current_buyer)):
    return db.query(Payment).filter(Payment.buyer_id == current_user.id).all()