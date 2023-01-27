from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Mapping, List

from database import get_db
import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(
    plain_password,
    hashed_password,
):
    return pwd_context.verify(plain_password, hashed_password)


def cretea_user(
    user: schemas.User,
    db: Session,
) -> None:
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        access_level=user.access_level,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_user(
    username: str,
    db: Session,
) -> Mapping:
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def update_user(
    username: str,
    user: schemas.User,
    db: Session,
) -> None:
    db.query(models.User).filter(
        models.User.username == username
    ).update(user.dict(exclude_none=True))
    db.commit()


def create_log(
    log: schemas.Log,
    db: Session,
) -> None:
    db_log = models.Log(
        service=log.service,
        username=log.username,
        ip_address=log.ip_address,
        content=log.content,
    )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)


def get_logs(
    db: Session,
    username: str = None,
) -> List[Mapping]:
    if username:
        logs = db.query(models.Log).filter(
            models.Log.username == username
        ).order_by(models.Log.created_at.desc()).all()
    else:
        logs = db.query(models.Log).order_by(models.Log.created_at.desc()).all()

    return logs
