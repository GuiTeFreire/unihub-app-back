from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from app.auth import get_password_hash

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.UsuarioOut)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_usuario_by_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    senha_hash = get_password_hash(usuario.senha)
    return crud.create_usuario(db, usuario, senha_hash)


@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    user = crud.get_usuario_by_id(db, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user