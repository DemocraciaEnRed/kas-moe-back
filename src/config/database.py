from os import getenv

from motor.motor_asyncio import AsyncIOMotorClient



client = AsyncIOMotorClient(
    getenv('DATABASE_URL'),
    uuidRepresentation="standard"
)

db = client["moe"]