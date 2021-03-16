from fastapi import APIRouter

from src.utils.users import manager



routes = APIRouter()

routes.include_router(manager.get_users_router(), prefix="/users", tags=["users"])