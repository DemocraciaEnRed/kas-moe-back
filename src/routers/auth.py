from fastapi import APIRouter

from src.utils.users import manager
from src.config.auth import cookie_authentication, jwt_authentication, Key
from src.services.auth import on_after_register, on_after_forgot_password, after_verification_request



routes = APIRouter()


routes.include_router(
    manager.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

routes.include_router(
    manager.get_auth_router(cookie_authentication), prefix="/auth/cookie", tags=["auth"]
)

routes.include_router(
    manager.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

routes.include_router(
    manager.get_reset_password_router(
        Key.JWT, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)

routes.include_router(
    manager.get_verify_router(
        Key.JWT, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)