from config.database import Base, database
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from schemas.user import UserDB


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)