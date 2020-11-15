import json

import pandas as pd
from app import auth, crud, models, schemas
from app.database import SessionLocal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
# templates = ''
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/beds")
def get_beds(
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

@router.put("/beds")
def update_beds(
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_username)
):  
    df = pd.read_sql("institute_master",con=db.bind)
    if df.shape[0]>1:
        crud.update_data(db)
    else:
        crud.initialise_data_in_db(db)

    return {"message": "data updated"}

@router.get("/beds/json")
def get_beds_json(request: Request):

    data = pd.read_csv("data.csv")

    hospital = data[data['institute_type']=='hospital']

    hospital = hospital.groupby(['institute', 'bed_type']).apply(
        lambda x: x[['total', 'occupied', 'vacant', 'queue']].to_dict('list')).reset_index()
    hospital_json = hospital.groupby('institute').apply(lambda x: dict(
        zip(x['bed_type'], x[0]))).to_json(orient="index")
    hospital_json = json.loads(hospital_json)


    return hospital_json
