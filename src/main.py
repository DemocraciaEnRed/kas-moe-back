from fastapi import FastAPI
from utils.app_exceptions import AppExceptionCase
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from utils.app_exceptions import app_exception_handler
from config.database import create_tables, database
from routers import auth, users


create_tables()

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(auth.routes)

app.include_router(users.routes)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
