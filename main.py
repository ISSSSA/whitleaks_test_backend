from fastapi import FastAPI
from routes import router
from config import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Vacancy CRUD API",
    description="API для управления вакансиями с hh.ru",
    version="1.0.0"
)
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
