from sqlalchemy.orm import Session

from . import models, schemas


def get_todo(db: Session, todo_id: int) -> models.Todo | None:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> list[models.Todo]:
    return db.query(models.Todo).order_by(models.Todo.id).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate) -> models.Todo | None:
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None
    for field, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, field, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> models.Todo | None:
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo