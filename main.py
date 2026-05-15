from fastapi import FastAPI

from app.modules.auth.api import auth_api
from app.modules.users.api import user_api
app = FastAPI()
app.include_router(auth_api.router)
app.include_router(user_api.router)