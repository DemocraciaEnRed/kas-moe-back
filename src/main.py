from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth, roll, users
from src.config.database import client, db


app = FastAPI(
    title=getenv('OAS_TITLE')
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv('ORIGINS'),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.routes)

app.include_router(users.routes)

app.include_router(roll.routes)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = db


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
