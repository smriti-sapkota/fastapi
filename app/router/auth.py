from fastapi import APIRouter, Depends , HTTPException, status
from .. import models , utils , oauth2
from ..database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select



router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=models.Token)
def login(db : SessionLocal, user_data : OAuth2PasswordRequestForm = Depends()) :
    user = db.exec(select(models.User).where(user_data.username == models.User.email)).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_data.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    token = oauth2.create_token({"users_id": user.id})

    return({"access_token":token, "token_type": "bearer"})
    
