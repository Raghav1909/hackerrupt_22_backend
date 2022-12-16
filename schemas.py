from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    is_admin: bool | None = False


class ProfileImage(BaseModel):
    id: int
    username: str
    url: HttpUrl


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    is_admin: bool = False
    date_of_birth: date | None = None
    designation: str | None = None
    phone_no: str | None = None
    professional_summary: str | None = None

class User(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    designation: str | None = None
    phone_no: str | None = None
    professional_summary: str | None = None
    
    class Config:
        orm_mode = True

class JobBase(BaseModel):
    company_name: str
    job_title: str
    job_description: str | None = None
    job_location: str | None = None
    job_salary: str | None = None
    job_posted_date: date | None = None
    job_closing_date: date | None = None


class CompanyBase(BaseModel):
    company_name: str
    company_logo: int | None = None
    company_website: str | None = None
    company_description: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: EmailStr