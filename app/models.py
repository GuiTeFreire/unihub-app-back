from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    matricula = Column(String, unique=True)

    atividades = relationship("Atividade", back_populates="usuario")
    grade = relationship("Grade", back_populates="usuario")

class Disciplina(Base):
    __tablename__ = "disciplinas"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    codigo = Column(String, unique=True)
    obrigatoria = Column(String)
    periodo = Column(String)

    grade = relationship("Grade", back_populates="disciplina")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"))

    professor = Column(String, nullable=True)
    sala = Column(String, nullable=True)
    faltas = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="grade")
    disciplina = relationship("Disciplina", back_populates="grade")

class Atividade(Base):
    __tablename__ = "atividades"
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    descricao = Column(String)
    disciplina = Column(String)
    status = Column(String)
    prazo = Column(Date)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="atividades")