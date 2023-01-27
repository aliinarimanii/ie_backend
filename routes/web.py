from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from sqlalchemy.orm import Session
import subprocess

from database import get_db
import schemas, crud, acl

router = APIRouter(
    prefix="/web-service",
    tags=["web service"],
)

@router.put(
    path="/start",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def start_web_service(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "echo 1234 | sudo -S service nginx start",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="web",
        username=user.username,
        ip_address=request.client.host,
        content="web service started",
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
async def stop_web_service(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "echo 1234 | sudo -S service nginx stop",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="web",
        username=user.username,
        ip_address=request.client.host,
        content="web service stopped",
    )

    crud.create_log(
        log=log,
        db=db,
    )


@router.get(
    path="/status"
)
async def get_web_service_status(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_read),
):
    proc = subprocess.Popen(
        "service nginx status",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="web",
        username=user.username,
        ip_address=request.client.host,
        content="web service status requested",
    )

    crud.create_log(
        log=log,
        db=db,
    )

    return outs


@router.put(
    path="/home-dir"
)
async def change_web_service_home_directory(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "TODO:",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="web",
        username=user.username,
        ip_address=request.client.host,
        content="home directory of web service changed",
    )

    crud.create_log(
        log=log,
        db=db,
    )
