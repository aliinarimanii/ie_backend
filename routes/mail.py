from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from sqlalchemy.orm import Session
import subprocess

from database import get_db
import schemas, crud, acl

router = APIRouter(
    prefix="/mail-service",
    tags=["mail service"],
)

@router.put(
    path="/start",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def start_mail_service(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "echo 1234 | sudo -S service postfix start",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="mail",
        username=user.username,
        ip_address=request.client.host,
        content="mail service started",
    )

    crud.create_log(
        log=log,
        db=db,
    )


@router.put(
    path="/stop",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def stop_mail_service(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "echo 1234 | sudo -S service postfix stop",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="mail",
        username=user.username,
        ip_address=request.client.host,
        content="mail service stopped",
    )

    crud.create_log(
        log=log,
        db=db,
    )


@router.get(
    path="/status"
)
async def get_mail_service_status(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_read),
):
    proc = subprocess.Popen(
        "service postfix status",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="mail",
        username=user.username,
        ip_address=request.client.host,
        content="mail service status requested",
    )

    crud.create_log(
        log=log,
        db=db,
    )

    return outs
