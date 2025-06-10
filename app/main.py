from fastapi import FastAPI
from app.database import Base, engine
from app.routers import usuarios, disciplinas, atividades, grades, login
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router, prefix="/usuarios")
app.include_router(disciplinas.router, prefix="/disciplinas")
app.include_router(atividades.router, prefix="/atividades")
app.include_router(grades.router, prefix="/grades")
app.include_router(login.router, prefix="/login")