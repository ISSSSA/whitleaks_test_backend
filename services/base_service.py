from sqlalchemy.orm import Session
from models.base_models import Vacancy
from schemas.base_schema import VacancyCreate, VacancyUpdate
import requests

HH_API_URL = "https://api.hh.ru/vacancies/"


def create_vacancy(db: Session, vacancy_data: VacancyCreate):
    response = requests.get(f"{HH_API_URL}{vacancy_data.hh_id}")
    if response.status_code != 200:
        return {"error": "Vacancy not found on HH.ru"}
    hh_data = response.json()

    vacancy = Vacancy(
        hh_id=vacancy_data.hh_id,
        company_name=hh_data['employer']['name'],
        company_address=hh_data['address']['raw'] if hh_data.get('address') else "",
        company_logo=hh_data['employer']['logo_urls']['original'] if hh_data['employer'].get('logo_urls') else "",
        vacancy_description=hh_data['description'],
        status="open"
    )
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return vacancy


def get_vacancy(db: Session, vacancy_id: int):
    return db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()


def update_vacancy(db: Session, vacancy_data: VacancyUpdate):
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_data.id).first()
    if not vacancy:
        return {"error": "Vacancy not found"}

    for key, value in vacancy_data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(vacancy, key, value)

    db.commit()
    db.refresh(vacancy)
    return vacancy


def delete_vacancy(db: Session, vacancy_id: int):
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if vacancy:
        db.delete(vacancy)
        db.commit()
        return {"message": "Vacancy deleted successfully"}
    return {"error": "Vacancy not found"}
