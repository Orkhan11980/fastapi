from typing import Optional, List

from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, utils
from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import UserCreate, UserCreateOut, UserDetail

router = APIRouter(
    prefix="/users",
     tags=['users']
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserCreateOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/get_all", response_model=List[UserCreateOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")
    return users


@router.get("/{id}", response_model=UserDetail)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found with {id}")
    return user
