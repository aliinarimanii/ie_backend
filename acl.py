from fastapi import Depends, HTTPException, status

from routers.token import get_current_user
import schemas

http_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="not allowed",
)

def allow_read(
    user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if user.access_level not in ["read", "write", "admin"]:
        raise http_exception
    
    return user


def allow_write(
    user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if user.access_level not in ["write", "admin"]:
        raise http_exception
    
    return user


def allow_admin(
    user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if user.access_level not in ["admin"]:
        raise http_exception
    
    return user
