from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/usuario/{usuario_id}", response_model=list[schemas.GradeOut])
def get_grade(usuario_id: int, db: Session = Depends(get_db)):
    return crud.get_grade_by_usuario(db, usuario_id)


@router.post("/usuario/{usuario_id}", response_model=schemas.GradeOut)
def add_grade_item(usuario_id: int, item: schemas.GradeCreate, db: Session = Depends(get_db)):
    return crud.add_disciplina_to_grade(db, usuario_id, item)


@router.put("/{grade_id}", response_model=schemas.GradeOut)
def update_grade_item(grade_id: int, updates: schemas.GradeCreate, db: Session = Depends(get_db)):
    grade = crud.update_grade(db, grade_id, updates)
    if not grade:
        raise HTTPException(status_code=404, detail="Item da grade não encontrado")
    return grade


@router.delete("/{grade_id}")
def delete_grade_item(grade_id: int, db: Session = Depends(get_db)):
    grade = crud.delete_grade_item(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Item da grade não encontrado")
    return {"ok": True}