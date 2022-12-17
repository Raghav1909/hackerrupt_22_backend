import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response,status
from database import get_db

router = APIRouter(
    prefix="/company",
    tags=["Company"],
)

# Company routes

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[schemas.CompanyBase])
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not allowed to access this page")

    companies = db.query(models.Company).offset(skip).limit(limit).all()
    return companies

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_company(company: schemas.CompanyBase, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to create companies")
    
    db_company = db.query(models.Company).filter(models.Company.company_name == company.company_name).first()
    
    if db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company already registered")
    
    new_company = models.Company(**company.dict())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return Response(status_code=status.HTTP_201_CREATED)

# Single Company Route

@router.get("/{name}",status_code=status.HTTP_200_OK,response_model=schemas.CompanyBase)
def get_company(name: str, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if name != current_user.company and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to view this company")
    
    db_company = db.query(models.Company).filter(models.Company.company_name == name).first()
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return db_company

@router.delete("/{name}",status_code=status.HTTP_200_OK)
def delete_company(name: str, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to delete companies")
    
    db_company = db.query(models.Company).filter(models.Company.company_name == name).first()
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    db.delete(db_company)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)