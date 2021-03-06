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


@router.post(
    "/patients", 
    status_code=status.HTTP_201_CREATED,
)
async def create_patients(
    patients : List[schemas.PatientInDb],
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    patients_count = crud.create_patients(db, patients)
    return {
        "message":f"{patients_count} new patients created."
    }


@router.put(
    "/patients", 
    status_code=status.HTTP_200_OK,
)
async def update_patients(
    patients : List[schemas.PatientInDb],
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    patients_count = crud.update_patients(db, patients)
    return {
        "message":f"Total patients {patients_count}."
    }

# patients
@router.get(
    "/patients", 
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.PatientInDb]    
)
async def read_patients(
    db: Session = Depends(get_db),
    # username: str = Depends(auth.get_current_username)
):
    patients = crud.get_patients(db)
    return patients

@router.delete(
    "/patients", 
    status_code=status.HTTP_200_OK,
)
async def delete_patients(
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    patients_count = crud.delete_patients(db)
    return {
        "message":f"Total of {patients_count} patients deleted."
    }



# Patient by id


@router.post("/patients/{patient_id}", status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_id : str,
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    db_patient = crud.get_patient_by_id(db, patient_id = patient_id)
    if db_patient:
        db.query(models.Patient).filter(models.Patient.patient_id == patient_id).delete()
        db.commit()
    flag, patient = crud.create_patient_by_id(db=db, patient=patient, patient_id = patient_id)
    if flag: 
        crud.update_data(db)
        return {
            "message": "Patient registered.",
            "data": patient
        }
    else:
        raise HTTPException(status_code=422, detail="Please provide either Hospital or CCC name.")

@router.put("/patients/{patient_id}", status_code=status.HTTP_200_OK)
async def update_patient(
    patient_id : str,
    patient: schemas.PatientUpdate,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):

    db_patient = crud.get_patient_by_id(db, patient_id= patient_id)        
    if db_patient:
        flag, patient = crud.update_patient_by_id(db=db, patient=patient, patient_id= patient_id)
        if flag:
            crud.update_data(db)
            return {
                "message": "Patient details updated.",
                "data": patient
            }
        else:
            raise HTTPException(status_code=422, detail="Please provide either Hospital or CCC name.")
    else:
        raise HTTPException(status_code=404, detail=f"Patient with Patient ID :{patient_id} does not exist.")

@router.get(
    "/patients/{patient_id}",
    status_code=status.HTTP_200_OK,
    response_model = schemas.PatientInDb,
)
async def read_patient(
    patient_id : str,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    db_patient = crud.get_patient_by_id(db, patient_id = patient_id)
    if db_patient:
        
        return db_patient
    else:
        raise HTTPException(status_code=404, detail=f"Patient with Patient ID :{patient_id} does not exist.")



@router.delete("/patients/{patient_id}")
async def delete_patient(
    patient_id : str,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):
    db_patient = crud.get_patient_by_id(db, patient_id = patient_id)
    if db_patient:
        flag = crud.delete_patient_by_id(db, patient_id = patient_id)
        
        if flag:
            crud.update_data(db)
            return {"message":"Patient removed and bed released."}
        else:
            raise HTTPException(status_code=422, detail="Please try again.")
    else:
        raise HTTPException(status_code=404, detail=f"Patient with Patient ID :{patient_id} does not exist.")
