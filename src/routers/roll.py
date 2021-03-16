from fastapi import APIRouter, Request, Depends, File, UploadFile

from pydantic import BaseModel, Field

from src.services import roll as Roll
from src.utils.users import manager
from src.schemas.user import User


routes = APIRouter()

roll = Roll.manage();

current_active_user = manager.current_user(active=True)


@routes.get("/list", tags=["roll"])
async def get_list(user: User = Depends(current_active_user)):
    response = await roll.read()
    print(response)
    return f"{response}"


@routes.post("/list", tags=["roll"])
async def update_list(request: Request, user: User = Depends(current_active_user), file: UploadFile = File(...)):
    await roll.write(file)
    return {"filename": file.filename}


@routes.delete("/list", tags=["roll"])
async def delete_list(request: Request, user: User = Depends(current_active_user)):
    return f"Is Admin?, {user.email}"

