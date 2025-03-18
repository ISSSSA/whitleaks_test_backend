from fastapi import FastAPI
from routes import router
from config import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vacancy CRUD API",
    description="API для управления вакансиями с hh.ru",
    version="1.0.0"
)

app.include_router(router)
