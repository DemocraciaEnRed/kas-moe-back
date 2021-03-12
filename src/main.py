import os
import motor.motor_asyncio
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.authentication import CookieAuthentication
from fastapi_users.db import MongoDBUserDatabase


""" To-Do: Implement proper assertion of environment variables
assert all([
    os.getenv(var)
    for var
    in [
        'DATABASE_URL'
        'JWT_SECRET'
        'MAILGUN_API_KEY'
    ]
])
"""



JWT_SECRET = os.getenv('JWT_SECRET')


auth_backends = []


jwt_authentication = JWTAuthentication(
    secret=JWT_SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)

auth_backends.append(jwt_authentication)


cookie_authentication = CookieAuthentication(
    secret=JWT_SECRET, lifetime_seconds=3600, name="x-moe-code-long"
)

auth_backends.append(cookie_authentication)



MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')



class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass



DATABASE_URL = os.getenv('DATABASE_URL')


client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)

db = client["database_name"]

collection = db["users"]

user_db = MongoDBUserDatabase(UserDB, collection)



def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")



app = FastAPI(title="MOE Authentication API")

origins = [
    "http://cyph.red",
    "https://cyph.red",
    "http://aglug.org",
    "http://aglug.org:3000",
    "https://glug.org",
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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