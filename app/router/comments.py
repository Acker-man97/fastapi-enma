from .. import schema, models, oauth2
from fastapi import HTTPException,status, Depends, APIRouter
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
router=APIRouter(
    tags=["Comments"],
    prefix="/comments")

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.CommentsOut)
def comments(comments: schema.Comments, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id == comments.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
   
    new_comment = models.Comments(user_id=current_user.id, **comments.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}", response_model=List[schema.CommentsOut])
def get_comment(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user) ):
    return db.query(models.Comments).filter(models.Comments.post_id == post_id).all()



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comments).filter(models.Comments.id == id)
    comment = comment_query.first()

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"comment with id {id} does not exist")
    if comment.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="not authorized to perform requested action")

    comment_query.delete(synchronize_session=False)
    db.commit()
    return
    
    