from fastapi import APIRouter
from utils.roles import manager
from utils.auth import on_after_register, on_after_forgot_password, after_verification_request
from config.auth import jwt_authentication, JWT


routes = APIRouter()

routes.include_router(
    manager.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

routes.include_router(
    manager.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

routes.include_router(
    manager.get_reset_password_router(
        JWT.KEY, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)

routes.include_router(
    manager.get_verify_router(
        JWT.KEY, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)
