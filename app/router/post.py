from fastapi import APIRouter , Depends, HTTPException , status , Response
from ..database import create_db_and_table,SessionLocal
from .. import models, oauth2
from typing import List , Optional
from sqlmodel import select, func

router = APIRouter(prefix='/posts', tags=["Posts"])


@router.get("/", response_model=List[models.PostOut])
def get_allposts(db:SessionLocal , limit: int = 10, skip: int = 0, search : Optional[str] = ''):

    posts = db.exec(select(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id ==models.Vote.post_id, isouter=True).group_by(models.Post.id).where(models.Post.title.contains(search)).limit(limit).offset(skip)).all()

    return posts

@router.get("/{id}",response_model =models.PostOut )
def get_postbyid(id:int , db: SessionLocal) :
    post = db.exec(select(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id ==models.Vote.post_id, isouter=True).group_by(models.Post.id).where(models.Post.id == id)).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id{id} not found.")
    
    return post

@router.post('/', response_model= models.PostResponse)
def create_post(db: SessionLocal,post_data: models.CreatePost, current_user : models.UserResponse = Depends(oauth2.get_current_user)):

    post = models.Post(owner_id = current_user.id, **post_data.model_dump())

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: SessionLocal , current_user: models.Post = Depends(oauth2.get_current_user)):
    post = db.get(models.Post , id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {id} not found.")
    
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="only owner is allowed to delete.")
    
    db.delete(post)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=models.PostResponse)
def update_post(id:int, db : SessionLocal , post_data: models.UpdatePost , current_user: models.UserResponse = Depends(oauth2.get_current_user)):
    post = db.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {id} not found.")
    
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="only owner is allowed to update.")
    
    new_post = post_data.model_dump()
    for key , value in new_post.items():
        setattr(post, key , value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post 

@router.patch("/{id}", response_model=models.PostResponse)
def patch_post(id:int, db : SessionLocal , post_data: models.PatchPost , current_user: models.UserResponse = Depends(oauth2.get_current_user)):
    post = db.get(models.Post, id)  
     

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {id} not found.")
    
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="only owner is allowed to patch.")
    
    new_post = post_data.model_dump()
    for key , value in new_post.items():
        if value != None:
         setattr(post, key , value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post 

