from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.base_service import create_vacancy, get_vacancy, update_vacancy, delete_vacancy
from schemas.base_schema import VacancyCreate, VacancyResponse, VacancyUpdate
from config import get_db

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(token: str = Security(oauth2_scheme)):
    payload = verify_token(token)
    new_token = create_access_token(data={"sub": payload["sub"]})
    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/api/v1/vacancy/create", response_model=VacancyResponse)
def create_vacancy_route(vacancy: VacancyCreate, db: Session = Depends(get_db)):
    return create_vacancy(db, vacancy)


@router.get("/api/v1/vacancy/get/{vacancy_id}", response_model=VacancyResponse)
def get_vacancy_route(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = get_vacancy(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy


@router.put("/update", response_model=VacancyUpdate)
def update_vacancy_endpoint(vacancy_data: VacancyUpdate, db: Session = Depends(get_db)):
    return update_vacancy(db, vacancy_data)


@router.delete("/api/v1/vacancy/delete/{vacancy_id}")
def delete_vacancy_route(vacancy_id: int, db: Session = Depends(get_db)):
    result = delete_vacancy(db, vacancy_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
