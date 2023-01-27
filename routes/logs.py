from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas, crud, acl

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    dependencies=[Depends(acl.allow_admin)],
)

@router.get(
    path="",
    response_model=List[schemas.Log],
)
async def get_all_logs(
    db: Session = Depends(get_db)
):
    return crud.get_logs(db=db)


@router.get(
    path="/{username}",
    response_model=List[schemas.Log],
)
async def get_user_logs(
    username: str = Path(default=...),
    db: Session = Depends(get_db),
):
    return crud.get_logs(
        db=db,
        username=username,
    )
