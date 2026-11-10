from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pathlib import Path

from utils.hash import ALGORITHM, SECRET_KEY, HashPassword, VerifyPassword

from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/auth', tags=['auth'])

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# PAGES
@router.get('/login-page')
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/register-page')
def render_login_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# ENDPOINTS
def auth_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not VerifyPassword(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }

    expires = datetime.now(timezone.utc) + expires_delta

    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return {'username': username, 'id': user_id, 'user_role': role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_deps, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = HashPassword(create_user_request.password),
        role = create_user_request.role,
        is_active = True,
        phone_number = create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()


@router.post('/token', response_model=Token)
async def login_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_deps):
    
    user = auth_user(form_data.username, form_data.password, db)

    print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}