import uuid

from typing import List, Optional, TypeVar

from pydantic import UUID4, BaseModel, EmailStr, validator

#from src.schemas.roll import UserDB
from src.config.database import db



collection = db["roll"]


""" To-Do: Add to classes for user-specific cases """

class Item(BaseModel):
    ID: int
    NAME: str