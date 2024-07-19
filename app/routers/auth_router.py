from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, database, oauth2, utils
from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import UserLogin
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login")
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id":  user.id})
    # print(access_token)
    return { "toke": access_token}
