from fastapi import FastAPI, APIRouter
from database import SessionLocal, engine

import models
from routers.users import router as users_router
from routers.web import router as web_router
from routers.mail import router as mail_router
from routers.dhcp import router as dhcp_router
from routers.logs import router as logs_router
from routers.token import router as token_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    swagger_ui_parameters={"docExpansion": "none"}
)

router = APIRouter(
    prefix="/api"
)

app.include_router(router=router)
app.include_router(router=users_router)
app.include_router(router=web_router)
app.include_router(router=mail_router)
app.include_router(router=dhcp_router)
app.include_router(router=logs_router)
app.include_router(router=token_router)
