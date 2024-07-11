from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional, List

from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import UserLogin

router = APIRouter()


@router.post("/login")
def user_login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    # access_token = oauth2.create_access_token(data={"user_id":  user.id})
    # print(access_token)
    return access_token
