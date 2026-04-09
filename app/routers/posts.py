from sys import prefix

from anyio import current_effective_deadline

from .. import models, schema, auth2
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from ..database import get_db
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
     prefix= "/posts",
     tags= ['posts']
)

# @router.get("/", response_model= List[schema.Post])
@router.get("/", response_model=List[schema.PostOut])
def posts(db : session = Depends(get_db), current_user : int = Depends(auth2.get_curent_user), limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    # cursor.execute("select * from post")
    # posts = cursor.fetchall()
    # posts = db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.post).filter(models.post.owner_id == current_user.id).all() #private serach
    posts = db.query(
        models.post,
        func.count(models.Votes.posts_id).label("votes")
    ).join(
        models.Votes, models.Votes.posts_id == models.post.id, isouter = True
    ).group_by(
        models.post.id
    ).filter(
        models.post.title.contains(search)
        ).limit(limit).offset(skip).all()
    return posts

@router.post("/createpost", status_code= status.HTTP_201_CREATED, response_model= schema.Post)
def create_post(post : schema.PostCreate, db : session = Depends(get_db), current_user : int = Depends(auth2.get_curent_user)):
    # cursor.execute("insert into public.post (title, content, published) values (%s, %s, %s ) returning *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

@router.get("/{id}", response_model= schema.PostOut)
def get_post(id : int, db : session = Depends(get_db)):
    # cursor.execute("select * from post where id  = %s", (id,))
    # post = cursor.fetchone()
    post = db.query(
        models.post,
        func.count(models.Votes.posts_id).label("votes")
    ).join(
        models.Votes, models.Votes.posts_id == models.post.id, isouter = True
    ).group_by(
        models.post.id
    ).filter(models.post.id == id).first()

    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f"post with {id} was not found")
    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : session = Depends(get_db), current_user : int = Depends(auth2.get_curent_user)):

    # cursor.execute("delete from post where id = %s returning *" , (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.post).filter(models.post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"post with id : {id} was not found")
    
    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code= status. HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id : int, updated_post : schema.PostCreate, db : session = Depends(get_db), current_user : int = Depends(auth2.get_curent_user)):
        # cursor.execute("update post set title = %s, content = %s, published = %s where id = %s returning *", (post.title, post.content, post.published, id,))
        # updated_post = cursor.fetchone()
        # conn.commit()
        post_query = db.query(models.post).filter(models.post.id == id)
        post = post_query.first()
        if post == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"post with id : {id} was not found")
        
        if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
        
        post_query.update(updated_post.dict(),synchronize_session = False )
        db.commit()
        return post_query.first() 