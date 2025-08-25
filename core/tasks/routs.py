# core/tasks/routs.py
from fastapi import status, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.db import get_db
from tasks.models import TaskModel
from fastapi import APIRouter
from math import ceil
from tasks.schemas import *

router = APIRouter(tags=["tasks"], prefix="/todo")


# ++++ CRUD with DB ++++

@router.get("/tasks",)
def retrieve_task_list(q: str | None = Query(default=None, alias="search", description="case-insensitive match on description", max_length=50),
                       completed : bool = Query(None, description="filter for completed"),
                       page: int = Query(1, ge=1, description="page number"),
                       limit: int = Query(10, le=50, description="number of items per page"),
                       db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if q:
        query = query.filter(TaskModel.title.ilike(q.strip()))
        # query = query.filter(TaskModel.title.ilike(f"%{q.strip()}%"))
    if completed is not None:
        query = query.filter_by(is_completed = completed)
    
    total_items = query.count()
    total_pages = ceil(total_items / limit) if total_items else 1
    
    # محاسبه offset از روی شماره صفحه
    offset = (page - 1) * limit
    
    results = query.offset(offset).limit(limit).all()
    
    # items = query.order_by(TaskModel.id.desc()).all()
    # return [{"id": e.id, "title": e.title, "description": e.description, "is_completed": e.is_completed, "create_date": e.create_date, "updated_date": e.updated_date} for e in items]
    # return query.all()
    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None,
        "result": results
    }

    
@router.post("/tasks", status_code=status.HTTP_201_CREATED)
# def create_task(title: str = Body(..., embed=True, min_length=3, max_length=150), description: str = Body(..., embed=True, min_length=3, max_length=500), is_completed: bool = Body(...), db: Session = Depends(get_db)):
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)):
    # exp = TaskModel(title=payload.title.strip(), description=payload.description.strip(), is_completed=payload.is_completed)
    exp = TaskModel(**payload.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    # return {"detail": "new task created", "task": {"id": exp.id, "title": exp.title, "description": exp.description, "is_completed": exp.is_completed, "create_date": exp.create_date}}
    return exp

@router.get("/tasks/{task_id}")
def retrieve_task_detail(task_id: int = Path(..., title="Task ID"), db: Session = Depends(get_db)):
    # exp = db.query(TaskModel).filter_by(id=task_id).one_or_none()
    exp = db.get(TaskModel, task_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")
    # return {"id": exp.id, "description": exp.description, "amount": exp.amount}
    return exp


@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
# def update_task_detail(task_id: int = Path(...), title: str = Body(..., embed=True, min_length=3, max_length=150), description: str = Body(..., embed=True, min_length=3, max_length=500), is_completed: bool = Body(...,), db: Session = Depends(get_db)):
def update_task_detail(payload: TaskUpdateSchema, task_id: int = Path(..., description="ID of the task to update"), db: Session = Depends(get_db)):
    # exp = db.query(TaskModel).filter_by(id=task_id).one_or_none()    
    exp = db.get(TaskModel, task_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")

    # snapshot before update
    before = TaskResponseSchema.model_validate(exp, from_attributes=True).model_dump()
    
    """
    exp.title = payload.title.strip()
    exp.description = payload.description.strip()
    exp.is_completed = payload.is_completed
    """
    
    # for field, value in payload.dict(exclude_unset=True).items():
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(exp, field, value)
    
    db.commit()
    db.refresh(exp)
    
    # after update
    after = TaskResponseSchema.model_validate(exp, from_attributes=True).model_dump()
    
    # return {"detail": "task updated", "task": {"id": exp.id, "description": exp.description, "amount": exp.amount}}
    # return {"detail": "task updated", "task": exp}
    return {"detail": f"task {task_id} updated", "before": before, "after": after}


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    exp = db.get(TaskModel, task_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")

    db.delete(exp)
    db.commit()
    return JSONResponse(content={"detail": f"task {task_id} deleted!"}, status_code=status.HTTP_200_OK)


