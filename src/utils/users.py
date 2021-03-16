from fastapi_users import FastAPIUsers

from src.models.user import user_db
from src.config.auth import auth_backends
from src.schemas.user import User, UserCreate, UserUpdate, UserDB


manager = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)