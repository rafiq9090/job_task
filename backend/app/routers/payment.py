from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_buyer
from ..models import Payment, Task, Project, User

router = APIRouter(prefix="/payments")

@router.post("/{task_id}")
def pay_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_buyer)):

    task = db.query(Task).join(Project).filter(
        Task.id == task_id, 
        Project.buyer_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == "paid":
        raise HTTPException(status_code=400, detail="This task has already been paid for.")

    if task.status != "submitted":
        raise HTTPException(status_code=400, detail="Task must be submitted before payment.")

    amount = task.hourly_rate * (task.hours_spent or 0)

   
    new_payment = Payment(
        task_id=task_id,
        buyer_id=current_user.id,
        amount=round(amount, 2), 
        status="completed"
    )

    task.status = "paid"

    db.add(new_payment)
    db.commit()

    return {
        "message": "Payment successful. Task solution is now unlocked.",
        "amount_paid": amount,
        "task_id": task_id
    }
@router.get("/")
def get_my_payments(db:Session=Depends(get_db), current_user: User=Depends(get_current_buyer)):
    return db.query(Payment).filter(Payment.buyer_id == current_user.id).all()