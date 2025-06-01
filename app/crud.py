from sqlalchemy.orm import Session
from app import models, schemas

# USUÁRIOS
def create_usuario(db: Session, user: schemas.UsuarioCreate, senha_hash: str):
    db_usuario = models.Usuario(
        nome=user.nome,
        email=user.email,
        senha_hash=senha_hash,
        matricula=user.matricula
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuario_by_id(db: Session, id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == id).first()


# DISCIPLINAS
def create_disciplina(db: Session, data: schemas.DisciplinaBase):
    db_disc = models.Disciplina(**data.dict())
    db.add(db_disc)
    db.commit()
    db.refresh(db_disc)
    return db_disc

def get_all_disciplinas(db: Session):
    return db.query(models.Disciplina).all()


# ATIVIDADES
def create_atividade(db: Session, data: schemas.AtividadeBase, usuario_id: int):
    db_atividade = models.Atividade(**data.dict(), usuario_id=usuario_id)
    db.add(db_atividade)
    db.commit()
    db.refresh(db_atividade)
    return db_atividade

def get_atividades_by_usuario(db: Session, usuario_id: int):
    return db.query(models.Atividade).filter(models.Atividade.usuario_id == usuario_id).all()

def update_atividade(db: Session, atividade_id: int, data: schemas.AtividadeBase):
    db_atividade = db.query(models.Atividade).filter(models.Atividade.id == atividade_id).first()
    if db_atividade:
        for key, value in data.dict().items():
            setattr(db_atividade, key, value)
        db.commit()
        db.refresh(db_atividade)
    return db_atividade

def delete_atividade(db: Session, atividade_id: int):
    db_atividade = db.query(models.Atividade).filter(models.Atividade.id == atividade_id).first()
    if db_atividade:
        db.delete(db_atividade)
        db.commit()
    return db_atividade

# GRADE
def get_grade_by_usuario(db: Session, usuario_id: int):
    return db.query(models.Grade).filter(models.Grade.usuario_id == usuario_id).all()

def add_disciplina_to_grade(db: Session, usuario_id: int, grade_data: schemas.GradeCreate):
    db_grade = models.Grade(
        usuario_id=usuario_id,
        disciplina_id=grade_data.disciplina_id,
        professor=grade_data.professor,
        sala=grade_data.sala,
        faltas=grade_data.faltas,
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def update_grade(db: Session, grade_id: int, updates: schemas.GradeCreate):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if db_grade:
        db_grade.professor = updates.professor
        db_grade.sala = updates.sala
        db_grade.faltas = updates.faltas
        db.commit()
        db.refresh(db_grade)
    return db_grade

def delete_grade_item(db: Session, grade_id: int):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if db_grade:
        db.delete(db_grade)
        db.commit()
    return db_grade