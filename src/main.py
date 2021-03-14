from os import getenv

import motor.motor_asyncio

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.authentication import CookieAuthentication
from fastapi_users.db import MongoDBUserDatabase

from src.services import email as Email



""" To-Do: Implement proper assertion of environment variables
assert all([
    getenv(var)
    for var
    in [
        'DATABASE_URL'
        'JWT_SECRET'
        'MAILGUN_API_KEY'
    ]
])
"""



JWT_SECRET = getenv('JWT_SECRET')


auth_backends = []


jwt_authentication = JWTAuthentication(
    secret=JWT_SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)

auth_backends.append(jwt_authentication)


cookie_authentication = CookieAuthentication(
    secret=JWT_SECRET, lifetime_seconds=3600, name="x-moe-code-long"
)

auth_backends.append(cookie_authentication)



class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass



DATABASE_URL = getenv('DATABASE_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)

db = client["database_name"]

collection = db["users"]

user_db = MongoDBUserDatabase(UserDB, collection)



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



app = FastAPI(title=getenv('OAS_TITLE'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv('ORIGINS'),
    #allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_auth_router(cookie_authentication),
    prefix="/auth/cookie", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth", tags=["auth"]
)

app.include_router(
    fastapi_users.get_reset_password_router(
        JWT_SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(
        JWT_SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users", tags=["users"]
)


current_active_user = fastapi_users.current_user(active=True)


@app.get("/list")
def get_list(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"