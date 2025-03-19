import os

from fastapi import FastAPI
from routes import router
from config import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

Base.metadata.create_all(bind=engine)
load_dotenv()
app = FastAPI(
    title="Vacancy CRUD API",
    description="API для управления вакансиями с hh.ru",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("origins"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
