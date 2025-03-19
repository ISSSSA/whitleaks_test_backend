from pydantic import BaseModel
from typing import Optional


class VacancyBase(BaseModel):
    hh_id: str


class VacancyCreate(VacancyBase):
    hh_id: str


class VacancyUpdate(BaseModel):
    id: int
    company_name: Optional[str]
    company_address: Optional[str]
    company_logo: Optional[str]
    vacancy_description: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True


class VacancyResponse(BaseModel):
    id: int
    company_name: str
    company_address: Optional[str]
    company_logo: Optional[str]
    vacancy_description: str
    status: str

    class Config:
        orm_mode = True
