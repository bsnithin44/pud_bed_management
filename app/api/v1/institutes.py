import json

import pandas as pd
from app import auth, crud, models, schemas
from app.database import SessionLocal
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# institutes

@router.post(
    "/institutes", 
    status_code=status.HTTP_201_CREATED,
)
async def create_institutes(
    institutes : List[schemas.InstituteInDb],    
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    institutes_count = crud.create_institutes(db, institutes)
    return {
        "message":f"New {institutes_count} institutes created."
    }

@router.get(
    "/institutes", 
    status_code=status.HTTP_200_OK,
    # response_model=List[schemas.InstituteInDb]    
)
async def read_institutes(
    db: Session = Depends(get_db),
    # username: str = Depends(auth.get_current_username)
):
    institutes = crud.get_institutes(db)
    return institutes

@router.put(
    "/institutes", 
    status_code=status.HTTP_200_OK,
)
async def update_institutes(
    institutes : List[schemas.InstituteInDb],    
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    institutes_count = crud.update_institutes(db, institutes)
    
    return {
        "message":f"Total institutes : {institutes_count}."
    }


@router.delete(
    "/institutes", 
    status_code=status.HTTP_200_OK,
)
async def delete_institutes(
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    institutes_count = crud.delete_institutes(db)
    return {
        "message":f"Total of {institutes_count} institutes deleted."
    }
