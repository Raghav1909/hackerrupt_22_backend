from fastapi import FastAPI, Depends, HTTPException, Response,status
from fastapi.middleware.cors import CORSMiddleware

import models
from database import SessionLocal, engine

from routers import users, auth, jobs, company

from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static',StaticFiles(directory='static'),name='static')

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(company.router)

@app.get("/")
async def root():
    return {"message": "PESCE backend"}
