import uuid
from motor_odm import Document
from typing import List, Optional, TypeVar
from pydantic import UUID4, BaseModel, EmailStr, validator

from src.config.database import db


class Roll(Document):
    class Mongo:
        collection = "roll"
    
    id: int
    name: str


Document.use(db)

collection = db["roll"]