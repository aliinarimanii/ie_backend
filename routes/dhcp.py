from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from sqlalchemy.orm import Session
import subprocess

from database import get_db
import schemas, crud, acl

router = APIRouter(
    prefix="/dhcp-service",
    tags=["dhcp service"],
)

@router.get(
    path="/start",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def start_dhcp_service(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "echo 1234 | sudo -S service isc-dhcp-server start",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="dhcp",
        username=user.username,
        ip_address=request.client.host,
        content="dhcp service started",
    )

    crud.create_log(
        log=log,
        db=db,
    )


@router.get(
    path="/stop",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def stop_dhcp_service(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "echo 1234 | sudo -S service isc-dhcp-server stop",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="dhcp",
        username=user.username,
        ip_address=request.client.host,
        content="dhcp service stopped",
    )

    crud.create_log(
        log=log,
        db=db,
    )


@router.get(
    path="/status"
)
async def get_dhcp_service_status(
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_read),
):
    proc = subprocess.Popen(
        "service isc-dhcp-server status",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="dhcp",
        username=user.username,
        ip_address=request.client.host,
        content="dhcp service status requested",
    )

    crud.create_log(
        log=log,
        db=db,
    )

    return outs


@router.put(
    path="/ip-range"
)
async def change_dhcp_service_ip_range(
    ip_address_range: schemas.IPAddressRange,
    request: Request,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(acl.allow_write),
):
    proc = subprocess.Popen(
        "echo 1234 | sudo -S cat /etc/dhcp/dhcpd.conf",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    
    outs, errs = proc.communicate()

    content = outs.decode("utf-8")

    substr = "subnet 192.168.10.0 netmask 255.255.255.0"
    left_index = content.index(substr)

    new_content = content[:left_index + 44]
    new_content += f"  range {ip_address_range.from_address} {ip_address_range.to_address};\n"

    substr = "  option"
    right_index = content[left_index + 45:].index(substr)

    new_content += content[left_index + right_index + 45:]

    file = open("dhcpd.conf", "w+")
    file.write(new_content)
    file.close()
    
    proc = subprocess.Popen(
        "echo 1234 | sudo -S mv ./dhcpd.conf /etc/dhcp/dhcpd.conf",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    outs, errs = proc.communicate()
    
    log = schemas.Log(
        service="dhcp",
        username=user.username,
        ip_address=request.client.host,
        content="ip address range of dhcp service changed",
    )

    crud.create_log(
        log=log,
        db=db,
    )
