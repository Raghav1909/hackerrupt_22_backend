import schemas, models, utils, oauth2, os
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response,status, Form
from database import get_db

from fastapi import File, UploadFile
from fastapi.responses import FileResponse
import secrets
from PIL import Image

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Users routes

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[schemas.User],)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not allowed to access this page")

    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Single User routes

@router.get("/{username}",status_code=status.HTTP_200_OK,response_model=schemas.User)
def get_user(username: str, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if username != current_user.username and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to view this user")
    
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to create users")
    
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return Response(status_code=status.HTTP_201_CREATED)

# @router.post("/",status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return Response(status_code=status.HTTP_201_CREATED)

@router.patch("/{username}",status_code=status.HTTP_200_OK)
def update_user(username: str, updated_user: schemas.UserUpdate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if username != updated_user.username and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to update this user")

    db_user_query = db.query(models.User).filter(models.User.username == username)
    db_user = db_user_query.first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_200_OK)

@router.delete("/{username}",status_code=status.HTTP_200_OK)
def delete_user(username: str, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to delete this user")
    
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()

    return Response(status_code=status.HTTP_200_OK)


# Proflie Photo routes

@router.get("/{username}/profile_photo",status_code=status.HTTP_200_OK)
def get_profile_photo(username: str, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if username != current_user.username and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to view this profile photo")
    
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_profile_photo = db.query(models.ProfilePhoto).filter(models.ProfilePhoto.username == username).first()
    if db_profile_photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile Photo not found")
    
    media_type = "image/jpeg"
    if db_profile_photo.img_name.split('.')[-1] == 'png':
        media_type = 'image/png'

    return FileResponse(f"static/profile_photos/{db_profile_photo.img_name}", media_type=media_type)

@router.post("/{username}/profile_photo",status_code=status.HTTP_200_OK)
def create_or_update_profile_photo(username: str,file: UploadFile = File(...), db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    if username != current_user.username and current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to create/update profile photo")
    
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_profile_photo = db.query(models.ProfilePhoto).filter(models.ProfilePhoto.username == username).first()
    id = -1
    if db_profile_photo:
        id = db_profile_photo.id
        db.delete(db_profile_photo)
        db.commit()
        os.remove(f"static/profile_photos/{db_profile_photo.img_name}")

    file_name = secrets.token_hex(8)
    file_extension = file.filename.split(".")[-1]
    
    if file_extension.lower() not in ("png", "jpg", "jpeg"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
    file_name = f"{file_name}.{file_extension}"
    with open(f"static/profile_photos/{file_name}", "wb") as buffer:
        image = Image.open(file.file)
        image = image.resize((200,200))
        if file_extension.lower() == "png":
            image.save(buffer, format="PNG")
        if file_extension.lower() == "jpg" or file_extension.lower() == "jpeg":
            image.save(buffer, format="JPEG")

    if id == - 1:
        new_profile_photo = models.ProfilePhoto(username = username,img_name = file_name)
    else:
        new_profile_photo = models.ProfilePhoto(id = id,username = username,img_name = file_name)
    db.add(new_profile_photo)
    db.commit()
    db.refresh(new_profile_photo)
    return Response(status_code=status.HTTP_201_CREATED)

