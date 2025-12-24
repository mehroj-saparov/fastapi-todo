from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, Field
from app.models.task import Priority


class TaskResponse(BaseModel):
    task_id: int
    name: Annotated[str, Field(min_length=3, max_length=64)]
    description: Optional[Annotated[str, Field(max_length=255)]] = None
    due_date: datetime
    priority: Priority
    category_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
