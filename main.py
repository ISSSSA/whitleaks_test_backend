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
    "http://localhost:3000",  # Укажите здесь адреса фронтенда или других разрешённых источников
    "https://example.com"  # Добавьте ваши нужные разрешённые домены
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Список доверенных доменов
    allow_credentials=True,  # Если нужно разрешить отправку cookie
    allow_methods=["*"],  # Разрешённые HTTP-методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Заголовки, которые могут отправляться
)

app.include_router(router)
