from fastapi_users.db import MongoDBUserDatabase

from src.schemas.user import UserDB
from src.config.database import db



collection = db["users"]

user_db = MongoDBUserDatabase(UserDB, collection)