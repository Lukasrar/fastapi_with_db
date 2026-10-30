from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from .auth import get_current_user

router = APIRouter(prefix='/admin', tags=['admin'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]

@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_deps, db: db_deps):
    if user is None or user.get('user_role') != 'admin' :
        raise HTTPException(status_code=401)