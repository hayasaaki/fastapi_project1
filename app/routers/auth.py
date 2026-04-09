
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import schema
from .. import database, models, utils, auth2

router =  APIRouter(tags= ['Authentication'])

@router.post("/login")
def login(user_credentials : OAuth2PasswordRequestForm = Depends() ,db : session = Depends(database.get_db)):
   user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
   if not user:
      raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
   if not utils.verify(user_credentials.password, user.password):
      raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials" )
   
   access_token = auth2.create_acces_token(data= {"user_id" : user.id})

   return {"access_token" : access_token, "token_type" : "bearer"}