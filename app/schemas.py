from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoCreate(TodoBase):
    """Fields accepted when creating a todo."""


class TodoUpdate(BaseModel):
    """Fields accepted when updating a todo. Everything is optional so
    callers can send a partial update."""

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)