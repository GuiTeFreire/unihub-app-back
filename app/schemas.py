from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    matricula: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    matricula: str

    class Config:
        orm_mode = True

class DisciplinaBase(BaseModel):
    nome: str
    codigo: str
    obrigatoria: str
    periodo: str

class DisciplinaOut(DisciplinaBase):
    id: int

    class Config:
        orm_mode = True

class GradeBase(BaseModel):
    disciplina_id: int
    professor: Optional[str] = None
    sala: Optional[str] = None
    faltas: Optional[int] = 0

class GradeCreate(GradeBase):
    pass

class GradeOut(GradeBase):
    id: int
    usuario_id: int
    disciplina: DisciplinaOut

    class Config:
        orm_mode = True

class AtividadeBase(BaseModel):
    titulo: str
    descricao: Optional[str]
    disciplina: str
    status: str
    prazo: date

class AtividadeOut(AtividadeBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int

class LoginData(BaseModel):
    email: str
    senha: str