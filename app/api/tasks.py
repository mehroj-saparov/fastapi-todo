from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..models.task import Task, Priority, Category
from ..models.user import User
from ..schemas.tasks import TaskResponse
from .deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    name: str = Form(...),
    category_id: int = Form(...),
    due_date: datetime = Form(...),
    description: str | None = Form(None),
    priority: Priority = Form(Priority.PRIORITY05),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    task = Task(
        name=name,
        description=description,
        due_date=due_date,
        priority=priority,
        category_id=category_id,
        user_id=user.user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[TaskResponse])
def get_task_list(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return (
        db.query(Task)
        .filter(Task.user_id == user.user_id)
        .order_by(Task.created_at.desc())
        .all()
    )


@router.get("/{pk}", response_model=TaskResponse)
def get_one_task(
    pk: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.task_id == pk, Task.user_id == user.user_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{pk}", response_model=TaskResponse)
def update_task(
    pk: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    due_date: datetime | None = Form(None),
    priority: Priority | None = Form(None),
    category_id: int | None = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.task_id == pk, Task.user_id == user.user_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if category_id is not None:
        category = db.query(Category).filter(Category.category_id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        task.category_id = category_id

    if name is not None:
        task.name = name
    if description is not None:
        task.description = description
    if due_date is not None:
        task.due_date = due_date
    if priority is not None:
        task.priority = priority

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    pk: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(Task.task_id == pk, Task.user_id == user.user_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
