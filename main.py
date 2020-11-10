import json
import time
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request

import auth
import crud
import models
import schemas
from database import SessionLocal, engine

app = FastAPI()
api_router = APIRouter()

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(
    router=auth.router,
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[Depends(dependency=auth.get_current_username)],
    responses={404: {"description": "Not found"}},
)

async def log_json(request: Request):

    print(await request.json())

@app.on_event("startup")
def startup_event():
    print('Initialising db')
    db = SessionLocal()
    crud.initialise_data_in_db(db)
    db.close()


@api_router.post("/block_bed", status_code=status.HTTP_201_CREATED)
async def block_bed(
    patient: schemas.PatientBase,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):

    db_patient = crud.get_patient(db, patient_id=patient.patient_id)
    allotted, in_queue = False, True
    if db_patient:
        db.query(models.Patient).filter(models.Patient.patient_id == patient.patient_id).delete()
        db.commit()
    flag, patient = crud.create_patient(db=db, patient=patient, allotted= allotted, in_queue= in_queue)
    if flag: 
        crud.update_data(db)
        return {"message":"Patient registered/ Bed blocked"}
    else:
        return {"message":"Try again with valid fields"}


@api_router.post("/allot_bed")
async def allot_bed(
    patient: schemas.PatientBase,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):

    db_patient = crud.get_patient(db, patient_id=patient.patient_id)
    allotted, in_queue = True, False
    if db_patient:
        db.query(models.Patient).filter(models.Patient.patient_id == patient.patient_id).delete()
        db.commit()
    flag, patient = crud.create_patient(db=db, patient=patient, allotted= allotted, in_queue= in_queue)
    if flag: 
        crud.update_data(db)
        return {"message":"Patient Updated and bed allotted"}
    else:
        return {"message":"Try again with valid fields"}


@api_router.put("/release_bed")
async def release_bed(
    patient: schemas.PatientBase,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):

    db_patient = crud.get_patient(db, patient_id=patient.patient_id)
    allotted, in_queue = False, False
        
    if db_patient:
        flag, patient = crud.update_patient(db=db, patient=patient, allotted= allotted, in_queue= in_queue)
        if flag:
            crud.update_data(db)
            return {"message":"Patient Updated and bed released"}
        else:
            return {"message":"Try again with valid fields"}
    else:
        raise HTTPException(status_code=404, detail=f"Patient with Patient ID :{patient.patient_id} does not exist")


@api_router.put("/update_bed")
async def update_bed(
    patient: schemas.PatientBase,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):

    db_patient = crud.get_patient(db, patient_id=patient.patient_id)
    
        
    if db_patient:
        allotted, in_queue = db_patient.allotted, db_patient.in_queue
        flag, patient = crud.update_patient(db=db, patient=patient, allotted= allotted, in_queue= in_queue)
        if flag:
            crud.update_data(db)
            return {"message":"Patient bed updated"}
        else:
            return {"message":"Try again with valid fields"}
    else:
        raise HTTPException(status_code=404, detail=f"Patient with Patient ID :{patient.patient_id} does not exist")


@app.get("/data")
def data(
    request: Request,
    db: Session = Depends(get_db),
    
):
    data = pd.read_sql("institute_master",con=db.bind)

    hospital = data[data['institute_type']=='hospital']

    hospital = hospital.groupby(['institute', 'bed_type']).apply(
        lambda x: x[['total', 'occupied', 'vacant', 'queue']].to_dict('list')).reset_index()
    hospital_json = hospital.groupby('institute').apply(lambda x: dict(
        zip(x['bed_type'], x[0]))).to_json(orient="index")
    hospital_json = json.loads(hospital_json)


    ccc = data[data['institute_type']=='ccc']

    ccc = ccc.groupby(['institute', 'bed_type']).apply(
        lambda x: x[['total', 'occupied', 'vacant', 'queue']].to_dict('list')).reset_index()
    ccc_json = ccc.groupby('institute').apply(lambda x: dict(
        zip(x['bed_type'], x[0]))).to_json(orient="index")
    ccc_json = json.loads(ccc_json)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "hospital_json": hospital_json,
        "ccc_json": ccc_json
    })


@app.get("/data/json")
def jsondata(request: Request):

    data = pd.read_csv("data.csv")

    hospital = data[data['institute_type']=='hospital']

    hospital = hospital.groupby(['institute', 'bed_type']).apply(
        lambda x: x[['total', 'occupied', 'vacant', 'queue']].to_dict('list')).reset_index()
    hospital_json = hospital.groupby('institute').apply(lambda x: dict(
        zip(x['bed_type'], x[0]))).to_json(orient="index")
    hospital_json = json.loads(hospital_json)


    return hospital_json


@app.get("/data/update")
def update_data_api(
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):  
    df = pd.read_sql("institute_master",con=db.bind)
    if df.shape[0]>1:
        crud.update_data(db)
    else:
        crud.initialise_data_in_db(db)

    return {"message": "data updated"}


app.include_router(api_router, dependencies=[Depends(log_json)])
