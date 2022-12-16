from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True,nullable=False)
    first_name = Column(String,nullable=True)
    last_name = Column(String,nullable= True)
    email = Column(String, unique=True, index=True,nullable=False)
    password = Column(String,nullable=False) # Store hashed password
    is_admin = Column(Boolean, default=False)
    date_of_birth = Column(Date,nullable=True)
    phone_no = Column(String, unique=True,nullable=True)
    professional_summary = Column(String,nullable=True)


class ProfilePhoto(Base):
    __tablename__ = "profile_photos"

    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey("users.username",ondelete= 'CASCADE'),nullable=False)
    img_name = Column(String,nullable=False)

    user = relationship("User")

class WorkExperience(Base):
    __tablename__ = "work_experiences"

    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey("users.username",ondelete= 'CASCADE'),nullable=False)
    company_name = Column(String,ForeignKey("companies.company_name",ondelete= 'CASCADE'),nullable=False)
    job_title = Column(String,nullable=False)
    start_date = Column(Date,nullable=False)
    end_date = Column(Date,nullable=False)
    description = Column(String,nullable=True)

    user = relationship("User")
    company = relationship("Company")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    company_name = Column(String, unique=True, index=True,nullable=False)
    company_logo = Column(String,nullable=True)
    company_website = Column(String,nullable=True)
    company_description = Column(String,nullable=True)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    company_name = Column(String, ForeignKey("companies.company_name",ondelete= 'CASCADE'),nullable=False)
    job_title = Column(String,nullable=False)
    job_description = Column(String,nullable=True)
    job_location = Column(String,nullable=True)
    job_salary = Column(String,nullable=True)
    applied_count = Column(Integer,nullable=False,default=0)
    job_posted_date = Column(Date,nullable=False)
    job_closing_date = Column(Date,nullable=False)

    company = relationship("Company")