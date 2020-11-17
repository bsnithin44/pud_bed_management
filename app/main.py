import json

import pandas as pd
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
# from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app import auth, crud, models, schemas
from app.api.v1 import beds, patients, institutes
from app.database import SessionLocal, engine

app = FastAPI()
api_router = APIRouter()

# templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    print('Initialising db')
    db = SessionLocal()
    crud.initialise_data_in_db(db)
    db.close()

app.include_router(
    router=auth.router,
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[Depends(dependency=auth.get_current_username)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    router=patients.router,
    prefix="/api/v1",
    tags=["Patients v1"],
    dependencies=[Depends(dependency=auth.get_current_username)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    router=institutes.router,
    prefix="/api/v1",
    tags=["Institutes v1"],
    dependencies=[Depends(dependency=auth.get_current_username)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    router=beds.router,
    prefix="/api/v1",
    tags=["Beds"],
    # dependencies=[Depends()],
    responses={404: {"description": "Not found"}},
)

async def log_json(request: Request):
    print(await request.json())


app.include_router(api_router, dependencies=[Depends(log_json)])
