from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    hh_id = Column(Integer, nullable=False)
    company_name = Column(String, nullable=False)
    company_address = Column(String, nullable=False)
    company_logo = Column(String, nullable=True)
    vacancy_description = Column(String, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)


