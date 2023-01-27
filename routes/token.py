from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status, APIRouter, Security, Response, Path
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Union

from database import get_db
import schemas, crud

router = APIRouter(
    prefix="/token",
    tags=["authentication"],
)

security = HTTPBearer()

SECRET_KEY = "291d9dc296b889f1350ba1760ca761a6ce564d336ae860e224c7e22cf295ee0a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(
    username: str,
    password: str,
    db: Session,
):
    user = crud.get_user(
        username=username,
        db=db,
    )
    
    if not user:
        return False
    if not crud.verify_password(
        plain_password=password,
        hashed_password=user.hashed_password,
    ):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    auth: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(auth.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(
        username=username,
        db=db,
    )
    if user is None:
        raise credentials_exception
    return user


@router.post(
    path="",
    response_model=schemas.Token,
)
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        form_data.username,
        form_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = user.__dict__
    token.update({
        "access_token": access_token,
        "token_type": "bearer",
    })
    return token
