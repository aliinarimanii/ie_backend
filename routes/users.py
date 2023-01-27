from fastapi import Depends, HTTPException, status, APIRouter, Response, Path
from sqlalchemy.orm import Session

from database import get_db
import schemas, crud, acl

router = APIRouter(
    prefix="/users",
    tags=["authentication"],
)

@router.post(
    path="/signup",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def create_user(
    user: schemas.User,
    db: Session = Depends(get_db),
):
    if crud.get_user(username=user.username, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    crud.cretea_user(
        user=user,
        db=db,
    )


@router.put(
    path="/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(acl.allow_admin)],
)
async def update_user(
    user: schemas.User,
    db: Session = Depends(get_db),
    username: str = Path(default=...),
):
    crud.update_user(
        username=username,
        user=user,
        db=db,
    )
