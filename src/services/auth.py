from fastapi import Request

from src.schemas.user import UserDB
from src.services import email as Email



email = Email.sender()


async def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered. An email will be sent.")
    values = { 
        "email": user.email
    }
    await email.on_register(values)


async def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")
    values = { 
        "email": user.email,
        "token": token
    }
    await email.on_recovery(values)


async def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")
    values = { 
        "email": user.email,
        "token": token
    }
    await email.on_verification(values)
