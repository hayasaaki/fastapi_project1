from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session
from .. import schema,database,models,auth2


router = APIRouter(
    prefix= "/vote",
    tags= ['Votes']
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote : schema.Vote, db : Session = Depends(database.get_db), current_user : int = Depends(auth2.get_curent_user)): 

    verify_post = db.query(models.post).filter(models.post.id == vote.post_id).first()
    if not verify_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id : {vote.post_id} does not exist")
    vote_query = db.query(models.Votes).filter(models.Votes.posts_id == vote.post_id, models.Votes.users_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'user {current_user.id}, has already voted on post {vote.post_id}')
        new_vote = models.Votes(posts_id = vote.post_id, users_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message" : "succesfuly added a vote"}
    else :
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Vote does not exist")
        vote_query.delete(synchronize_session= False)
        db.commit()

        return {"message" : "succesfully deleted the vote"}