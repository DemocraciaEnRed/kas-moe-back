from fastapi_users import models
from pydantic import validator



class User(models.BaseUser):
    """
    USER OBJECT ATTRS:
    - Fields that go here must have a value (you can populate them in UserDB or UserCreate)
    - This reprents the user object. If you want any user data to be a part of that object
      besides BaseUser fields then add them here (TEST IF TRUE).
    - If you're fine with the BaseUser fields then leave this blank
    username: str
    timezone: str
    """


class UserCreate(models.BaseUserCreate):
    @validator('password')
    def valid_password(cls, v: str):
        if len(v) < 6:
            raise ValueError('Password should be at least 6 characters')
        return v


class UserUpdate(User, models.BaseUserUpdate):
    """
    ToDo: Define fields user can update
    """
    pass


class UserDB(User, models.BaseUserDB):
    """
    ASSIGN DEFAULTS:
    - Use this to assign defaults via = or @validator
    username: Optional[str] = ''
    timezone: Optional[str] = Field('+08:00', max_length=10)
    """
    
    """"
    @validator('fieldname', pre=True, always=True)
    def demo(cls, val):
        return val or other_value
    """