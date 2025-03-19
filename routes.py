from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from models.base_models import User
from services.auth_service import create_access_token, verify_token, oauth2_scheme
from services.base_service import create_vacancy, get_vacancy, update_vacancy, delete_vacancy
from schemas.base_schema import VacancyCreate, VacancyResponse, VacancyUpdate
from config import get_db
import jwt
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/api/v1/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or user.password_hash != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    print({"access_token": access_token, "token_type": "bearer"})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/v1/refresh")
def refresh_token(token: str = Security(oauth2_scheme)):
    payload = verify_token(token)
    new_token = create_access_token(data={"sub": payload["sub"]})
    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/api/v1/vacancy/create", response_model=VacancyResponse)
def create_vacancy_route(vacancy: VacancyCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)
                         ):
    user = token.get("username")
    return create_vacancy(db, vacancy)


@router.get("/api/v1/vacancy/get/{vacancy_id}", response_model=VacancyResponse)
def get_vacancy_route(vacancy_id: int, db: Session = Depends(get_db), token: dict = Depends(verify_token)
                      ):
    user = token.get("username")
    vacancy = get_vacancy(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy


@router.put("/api/v1/vacancy/update", response_model=VacancyUpdate)
def update_vacancy_endpoint(vacancy_data: VacancyUpdate, db: Session = Depends(get_db),
                            token: dict = Depends(verify_token)
                            ):
    user = token.get("username")
    return update_vacancy(db, vacancy_data)


@router.delete("/api/v1/vacancy/delete/{vacancy_id}")
def delete_vacancy_route(vacancy_id: int, db: Session = Depends(get_db), token: dict = Depends(verify_token)
                         ):
    user = token.get("username")
    result = delete_vacancy(db, vacancy_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
