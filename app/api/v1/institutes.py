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


# # institutes
# @router.get(
#     "/institutes", 
#     status_code=status.HTTP_200_OK,
#     response_model=List[schemas.InstituteIn]    
# )
# async def get_institutes(
#     db: Session = Depends(get_db),
#     # username: str = Depends(auth.get_current_username)
# ):
#     institutes = crud.get_institutes(db)
#     return institutes


# @router.post(
#     "/institutes", 
#     status_code=status.HTTP_201_CREATED,
# )
# async def post_institutes(
#     db: Session = Depends(get_db),
#     institutes = List[schemas.PatientInDb],
#     username: str = Depends(auth.get_current_username)
# ):
#     institutes_count = crud.create_institutes(db, institutes)
#     return {
#         "message":f"New {institutes_count} institutes created."
#     }


# @router.put(
#     "/institutes", 
#     status_code=status.HTTP_200_OK,
# )
# async def put_institutes(
#     db: Session = Depends(get_db),
#     institutes = List[schemas.PatientInDb],
#     username: str = Depends(auth.get_current_username)
# ):
#     institutes_count = crud.add_institutes(db, institutes)
#     return {
#         "message":f"Total institutes : {institutes_count}."
#     }


# @router.delete(
#     "/institutes", 
#     status_code=status.HTTP_200_OK,
# )
# async def delete_institutes(
#     db: Session = Depends(get_db),
#     username: str = Depends(auth.get_current_username)
# ):
#     institutes_count = crud.delete_institutes(db)
#     return {
#         "message":f"Total of {institutes_count} institutes deleted."
#     }

# # Institute by name

# @router.get(
#     "/institutes/{institute_name}",
#     status_code=status.HTTP_200_OK,
#     response_model = schemas.InstituteInDb,
# )
# async def get_patient(
#     institute_name : str,
#     db: Session = Depends(get_db),
#     username: str = Depends(auth.get_current_username)
# ):
#     db_institute = crud.get_institute_by_name(db, institute_name = institute_name)
#     if db_institute:
#         return db_patient
#     else:
#         raise HTTPException(status_code=404, detail=f"Institute with name :{institute_name} does not exist.")


# @router.post(
#     "/institutes/{institute_name}", 
#     status_code=status.HTTP_201_CREATED
#     )
# async def create_patient(
#     institute_name : str,
#     institute: schemas.InstituteBase,
#     db: Session = Depends(get_db),
#     username: str = Depends(auth.get_current_username)
# ):
#     db_institute = crud.get_institute_by_name(db, institute_name = institute_name)
#     if db_institute:
#         raise HTTPException(status_code=422, detail=f"Institute with name {institute_name} already exists.")
#     else:
#         flag, patient = crud.create_institute(db=db, institute=institute, institute_name = institute_name)


# @router.put(
#     "/institutes/{institute_name}", 
#     status_code=status.HTTP_200_OK
#     )
# async def update_patient(
#     institute_name : str,
#     institute: schemas.InstituteBase,
#     db: Session = Depends(get_db),
#     username: str = Depends(auth.get_current_username)
# ):
#     db_institute = crud.get_institute_by_name(db, institute_name = institute_name)
#     if db_institute:
#         flag, patient = crud.update_institute(db=db, institute=institute, institute_name = institute_name)
#         return {"message":f"Institute {institute_name} Updated."}
#     else:
#         raise HTTPException(status_code=422, detail=f"Institute with name {institute_name} does not exist.")


# @router.delete("(
#     "/institutes/{institute_name}", 
#     status_code=status.HTTP_200_OK
#     )
# async def delete_patient(
#     institute_name : str,
#     db: Session = Depends(get_db),
#     username: str = Depends(auth.get_current_username)
# ):
#     db_institute = crud.get_institute_by_name(db, institute_name = institute_name)
#     if db_institute:
#         db.query(models.Patient).filter(models.Patient.patient_id == patient_id).delete()
#         db.commit()
#         return {"message":"Institute and  removed and bed released."}
#     else:
#         raise HTTPException(status_code=404, detail=f"Patient with Patient ID :{patient_id} does not exist.")
