from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.DisciplinaOut)
def criar_disciplina(data: schemas.DisciplinaBase, db: Session = Depends(get_db)):
    return crud.create_disciplina(db, data)


@router.get("/", response_model=list[schemas.DisciplinaOut])
def listar_disciplinas(db: Session = Depends(get_db)):
    return crud.get_all_disciplinas(db)

@router.post("/batch")
def criar_varias_disciplinas(lista: list[schemas.DisciplinaBase], db: Session = Depends(get_db)):
    criadas = []
    for item in lista:
        if not db.query(models.Disciplina).filter_by(codigo=item.codigo).first():
            nova = models.Disciplina(**item.dict())
            db.add(nova)
            criadas.append(nova)
    db.commit()
    return {"criadas": len(criadas)}