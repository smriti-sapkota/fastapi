from fastapi import APIRouter, HTTPException , status , Depends 
from ..database import SessionLocal
from .. import models , database , oauth2
from sqlmodel import select

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote_post( vote: models.VoteBase, db:SessionLocal , current_user : int = Depends(oauth2.get_current_user)) :  #user must be logged in to vote
    
    post = db.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with id{vote.post_id}not found')
    
    found_vote = db.exec(select(models.Vote).where(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)).first()
    
    if vote.direction == 1 :
        if found_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail=f'user{current_user.id} has already voted on post{vote.post_id}')
        new_vote = models.Vote(post_id= vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()
        return {"message": "vote added successfully"}
       
    else :
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vote doesnot exits.')
        
        db.delete(found_vote)
        db.commit()
        return {'message' : 'vote removed successfully'}