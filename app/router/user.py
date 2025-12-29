from fastapi import APIRouter,status, HTTPException
from .. import models,utils
from ..database import SessionLocal

router = APIRouter(prefix="/users" , tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=models.UserResponse)
def create_user(user_data: models.UserCreate , db: SessionLocal):
    hashed_password = utils.hash(user_data.password)
    user_data.password = hashed_password

    user = models.User.model_validate(user_data)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", response_model=models.UserResponse)
def get_user(id:int , db: SessionLocal):
    user = db.get(models.User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id{id} is not found")
    
    return user