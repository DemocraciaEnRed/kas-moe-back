from fastapi_users import FastAPIUsers
from models.user import user_db
from config.auth import jwt_authentication
from schemas.user import User, UserCreate, UserUpdate, UserDB


manager = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)