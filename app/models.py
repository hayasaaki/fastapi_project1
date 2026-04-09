from email.policy import default

import string

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.sql.expression import null
from .database import base
from sqlalchemy.orm import relationship

class post(base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key =  True, nullable = False)
    title = Column(String, nullable = False) 
    content = Column(String, nullable = False)
    published = Column (Boolean, nullable= False, server_default= 'True')
    owner_id = Column (Integer, ForeignKey ("users.id", ondelete= "CASCADE"), nullable= False)

    owner = relationship("User")    

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key =  True, nullable = False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('now()'))

class Votes(base):
    __tablename__ = "votes"
    users_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key= True)
    posts_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key= True)