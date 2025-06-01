from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app import crud, schemas
from app.database import SessionLocal
from datetime import timedelta

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_usuario_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Email ou senha inválidos")
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario_id": user.id
    }
