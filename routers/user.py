from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, Field
from models import Todos, Users
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated

from utils.hash import HashPassword, VerifyPassword
from .auth import get_current_user

router = APIRouter(prefix='/user', tags=['user'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=4)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    role: str
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]

@router.get('/get-user', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: user_deps, db: db_deps):
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_model


@router.put('/change-password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_deps, db: db_deps, change_pass_request:ChangePasswordRequest):    
    if change_pass_request.current_password is None:
        raise HTTPException(status_code=401, detail="Must send the current password")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")


    if VerifyPassword(change_pass_request.current_password, user_model.hashed_password):
        user_model.hashed_password = HashPassword(change_pass_request.new_password)

        db.add(user_model)
        db.commit()
    else:
        raise HTTPException(status_code=500, detail="An error has occured")
  

@router.put('/change-phone-number/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumber(user: user_deps, db: db_deps, phone_number: str):    

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")


    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()
  









    

