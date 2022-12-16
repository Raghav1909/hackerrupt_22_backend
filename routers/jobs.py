import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response,status
from database import get_db

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

# Jobs routes

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[schemas.JobBase])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not allowed to access this page")

    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_job(job: schemas.JobBase, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to create jobs")
    
    db_job = db.query(models.Job).filter(models.Job.name == job.name).first()
    
    if db_job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job already registered")
    
    new_job = models.Job(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return Response(status_code=status.HTTP_201_CREATED)

# Single Job Route

@router.get("/{name}",status_code=status.HTTP_200_OK,response_model=schemas.JobBase)
def get_job(name: str, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if name != current_user.username and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to view this job")
    
    db_job = db.query(models.Job).filter(models.Job.name == name).first()
    if db_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return db_job

@router.delete("/{name}",status_code=status.HTTP_200_OK)
def delete_job(name: str, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to delete jobs")
    
    db_job = db.query(models.Job).filter(models.Job.name == name).first()
    if db_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)