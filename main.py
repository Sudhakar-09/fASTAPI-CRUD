# Importing necessary modules from FastAPI and other libraries
from fastapi import FastAPI, HTTPException, Depends, status  # FastAPI framework, HTTP exceptions, dependency injection, and HTTP status codes
from pydantic import BaseModel  # For defining data validation and schemas
from typing import Annotated  # Provides type hinting with additional metadata (introduced in Python 3.9+)
import models  # Custom module (assumed to contain SQLAlchemy models for database tables)
from database import engine, sessionLocal  # Custom module (assumed to contain database engine and session factory setup)
from sqlalchemy.orm import Session  # Provides session management for database interaction

# Create an instance of the FastAPI application
app = FastAPI()

# Create database tables using SQLAlchemy's metadata
models.Base.metadata.create_all(bind=engine)

# Pydantic model for posts, defining schema and validation rules
class postBase(BaseModel):
    title: str  # The title of the post (string type)
    content: str  # The content of the post (string type)
    user_id: int  # ID of the user who created the post (integer type)

# Pydantic model for users, defining schema and validation rules
class userBase(BaseModel):
    username: str  # The username of the user (string type)

# Dependency function to manage database session lifecycle
def get_db():
    db = sessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to the dependent functions
    finally:
        db.close()  # Ensure the session is closed after use

# Dependency type hint using `Annotated` to integrate dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

# Endpoint to create a post (HTTP POST request)
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: postBase, db: db_dependency):
    # Create a new Post object using the data from the request body
    db_post = models.Post(**post.dict())
    db.add(db_post)  # Add the new post to the database session
    db.commit()  # Commit the transaction to save changes

# Endpoint to read a post by ID (HTTP GET request)
@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    # Query the database for a post with the given ID
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:  # Check if the post exists
        HTTPException(status_code=404, detail='POST WAS NOT FOUND')  # Raise 404 error if not found
    return post  # Return the post data

# Endpoint to create a user (HTTP POST request)
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: userBase, db: db_dependency):
    # Create a new User object using the data from the request body
    db_user = models.User(**user.dict())
    db.add(db_user)  # Add the new user to the database session
    db.commit()  # Commit the transaction to save changes

# Endpoint to read a user by ID (HTTP GET request)
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    # Query the database for a user with the given ID
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:  # Check if the user exists
        raise HTTPException(status_code=404, detail='User not found')  # Raise 404 error if not found
    return user  # Return the user data

# Endpoint to delete a post by ID (HTTP DELETE request)
@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    # Query the database for a post with the given ID
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:  # Check if the post exists
        raise HTTPException(status_code=404, detail="POST WAS NOT FOUND")  # Raise 404 error if not found
    db.delete(db_post)  # Delete the post from the database session
    db.commit()  # Commit the transaction to save changes

# Endpoint to delete a user by ID (HTTP DELETE request)
@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    # Query the database for a user with the given ID
    delete_user = db.query(models.User).filter(models.User.id == user_id).first()
    if delete_user is None:  # Check if the user exists
        raise HTTPException(status_code=404, detail="USER WAS NOT FOUND")  # Raise 404 error if not found
    db.delete(delete_user)  # Delete the user from the database session
    db.commit()  # Commit the transaction to save changes
