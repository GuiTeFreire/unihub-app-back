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


@router.post("/usuario/{usuario_id}", response_model=schemas.AtividadeOut)
def criar_atividade(usuario_id: int, data: schemas.AtividadeBase, db: Session = Depends(get_db)):
    return crud.create_atividade(db, data, usuario_id)


@router.get("/usuario/{usuario_id}", response_model=list[schemas.AtividadeOut])
def listar_atividades(usuario_id: int, db: Session = Depends(get_db)):
    return crud.get_atividades_by_usuario(db, usuario_id)


@router.put("/{atividade_id}", response_model=schemas.AtividadeOut)
def atualizar_atividade(atividade_id: int, data: schemas.AtividadeBase, db: Session = Depends(get_db)):
    atividade = crud.update_atividade(db, atividade_id, data)
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return atividade


@router.delete("/{atividade_id}")
def excluir_atividade(atividade_id: int, db: Session = Depends(get_db)):
    atividade = crud.delete_atividade(db, atividade_id)
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return {"ok": True}