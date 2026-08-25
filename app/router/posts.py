from .. import schema, models, utilis, oauth2
from fastapi import HTTPException,status, Depends, APIRouter
from ..database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
prefix="/posts",
tags=["Post"]
)


@router.get("/", response_model=List[schema.PostOut])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    likes_count = db.query(models.Likes.post_id, func.count(models.Likes.post_id).label("likes")).group_by(models.Likes.post_id).subquery()


    comments_count = db.query(models.Comments.post_id, func.count(models.Comments.post_id).label("comments")).group_by(models.Comments.post_id).subquery()


    posts = db.query(models.Posts,func.coalesce(likes_count.c.likes, 0).label("likes"),func.coalesce(comments_count.c.comments, 0).label("comments")).outerjoin(likes_count, likes_count.c.post_id == models.Posts.id).outerjoin(comments_count, comments_count.c.post_id == models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts




@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schema.Response)
def create_post(post: schema.Posts, db: Session = Depends(get_db), current_user: schema.TokenData = Depends(oauth2.get_current_user)):
    new_post = models.Posts(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/{id}", response_model=schema.PostOut)
def get_id_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    likes_count = db.query(models.Likes.post_id, func.count(models.Likes.post_id).label("likes")).group_by(models.Likes.post_id).subquery()
    
    
    comments_count = db.query(models.Comments.post_id, func.count(models.Comments.post_id).label("comments")).group_by(models.Comments.post_id).subquery()
    post = db.query(models.Posts,func.coalesce(likes_count.c.likes, 0).label("likes"),func.coalesce(comments_count.c.comments, 0).label("comments")).outerjoin(likes_count, likes_count.c.post_id == models.Posts.id).outerjoin(comments_count, comments_count.c.post_id == models.Posts.id).filter(models.Posts.id == id).first()
    # post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} Not Found",
        )
    return  post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schema.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post  Not Found")

    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform Requested")
 
    post_query.delete(synchronize_session=False)
    db.commit()

    
@router.put("/{id}", response_model=schema.Response)
def update_post(id: int, updated_post: schema.Posts, db: Session = Depends(get_db), current_user: schema.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()

    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post  Not Found")        

    if post.owner_id != current_user.id:  # type: ignore
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform Requested")
     
    post_query.update(updated_post.dict(), synchronize_session=False) # type: ignore
    db.commit()
    return  post_query.first()


