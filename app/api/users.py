from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..models.user import User
from ..models.task import Task, TaskStatus
from ..schemas.user import UserProfile
from .deps import get_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", response_model=UserProfile)
def profile(
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    result = {
        "tasks_count": user.tasks.count(),
        "tasks_todo": user.tasks.filter(Task.status == TaskStatus.TODO).count(),
        "tasks_doing": user.tasks.filter(Task.status == TaskStatus.DOING).count(),
        "tasks_done": user.tasks.filter(Task.status == TaskStatus.DONE).count(),
    }

    return {"user": user, "result": result}