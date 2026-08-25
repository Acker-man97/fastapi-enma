from .. import schema, models, utilis, oauth2
from fastapi import FastAPI,HTTPException,status, Depends, APIRouter
from ..database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["VOTE"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def likes(likes: schema.Likes, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id == likes.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
   
    likes_query = db.query(models.Likes).filter(models.Likes.post_id==likes.post_id, models.Likes.user_id==current_user.id)
    found_likes = likes_query.first()
    if (likes.dir == 1):
        if found_likes:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has already voted on post{likes.post_id}")
        new_vote = models.Likes(post_id = likes.post_id, user_id = current_user.id )       
        db.add(new_vote)
        db.commit()
    else:
        if not found_likes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")

        likes_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "Deleted Like"}