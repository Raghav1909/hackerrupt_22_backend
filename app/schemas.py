from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, Union

class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    is_admin: Union[bool,None] = False


class ProfileImage(BaseModel):
    id: int
    username: str
    url: HttpUrl


class UserUpdate(UserBase):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    date_of_birth: Union[date, None] = None
    phone_no: Union[str, None] = None
    professional_summary: Union[str, None] = None

class User(UserCreate):
    first_name: Union[str,None] = None
    last_name: Union[str,None] = None
    date_of_birth: Union[date,None]= None
    phone_no: Union[str,None] = None
    professional_summary: Union[str,None] = None
    
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    email: EmailStr
    username: str
    first_name: Union[str,None] = None 
    last_name: Union[str,None] = None
    date_of_birth: Union[date,None]= None
    phone_no: Union[str,None] = None
    professional_summary: Union[str,None] = None
    is_admin: bool

    class Config:
        orm_mode = True


class JobBase(BaseModel):
    company_name: str
    job_title: str
    job_description: Union[str,None] = None
    job_location: Union[str,None] = None
    job_salary: Union[str,None] = None
    job_posted_date: Union[date,None] = None
    job_closing_date: Union[date,None] = None

    class Config:
        orm_mode = True


class CompanyBase(BaseModel):
    company_name: Union[str,None] = None
    company_logo: Union[int,None]= None
    company_website: Union[str,None] = None
    company_description: Union[str,None] = None

    class Config:
        orm_mode = True

class CompanyOut(BaseModel):
    company_name: str
    company_website: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: EmailStr