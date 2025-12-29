from jose import JWTError , jwt
from datetime import datetime , timedelta
from . import models,database

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException , status
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME = settings.expiration_time


def create_token(payload : dict):
    to_encode = payload.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY , algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str , credentials_exception):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])

        id : int = payload.get("users_id")
        if not id:
            raise credentials_exception
        token_data = models.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(db:database.SessionLocal, token:str = Depends(oauth2_scheme)) : 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldnot validate user", headers={"WWW-Authenticate": "Bearer"})

    payload = verify_access_token(token , credentials_exception)

    user = db.get(models.User , payload.id)

    return user




  






    





