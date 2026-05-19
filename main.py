import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.modules.auth.api import auth_api
from app.modules.users.api import user_api
from app.modules.groups.api import group_api
from app.modules.tasks.api import task_api
from app.modules.notification.api import notification_api
app = FastAPI()
app.include_router(auth_api.router)
app.include_router(user_api.router)
app.include_router(group_api.router)
app.include_router(task_api.router)
app.include_router(notification_api.router)
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
