from fastapi import FastAPI
from . import models
from .database import engine 
from .routers import user, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
import logging

models.Base.metadata.create_all(bind = engine)
app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)