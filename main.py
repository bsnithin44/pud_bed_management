import json
import secrets
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request

from serects import *

security = HTTPBasic()
app = FastAPI()
api_router = APIRouter()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class Patient(BaseModel):
    ticket_id: str
    patient_id: str
    hospital: str
    bed_type: Optional[str] = 'no_bed_type'
    name: Optional[str] = None


def update_data():
    df_data = pd.read_csv("data.csv")
    df_patient = pd.read_csv("patient.csv")
    df_patient['patient_id'] = df_patient['patient_id'].astype(str)

    for hospital in df_data.hospital.unique():
        df_p1 = df_patient[df_patient['hospital'] == hospital]

        for bed_type in ('Oxygen Bed', 'Isolation Bed', 'Ventilator Bed'):
            df_p1_b = df_p1[df_p1['bed_type'] == bed_type]
            index_ = df_data[(df_data['hospital'] == hospital) & (
                df_data['bed_type'] == bed_type)].index

            occupied = df_p1_b[df_p1_b['alloted']
                               == True]['patient_id'].count()
            queue = df_p1_b[df_p1_b['in_queue'] == True]['patient_id'].count()
            total = df_data.iloc[index_]['total']
            vacant = total - occupied
            df_data.loc[index_, ('occupied', 'vacant', 'queue')] = [
                occupied, vacant, queue]

        df_p1_q = df_p1[df_p1['in_queue'] == True]
        queue_not_decided = df_p1_q[(
            df_p1_q['bed_type'] == 'no_bed_type')]['patient_id'].count()
        df_data.loc[(df_data['hospital'] == hospital) & (
            df_data['bed_type'] == bed_type), 'queue'] = queue_not_decided

    df_data.to_csv("data.csv", index=False)


def update_patient(alloted, in_queue, patient):
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_patient = pd.read_csv("patient.csv")
    df_patient['patient_id'] = df_patient['patient_id'].astype(str)

    # alloted = False
    # in_queue = True
    data = [
        patient.patient_id, patient.ticket_id, patient.hospital,
        patient.name, patient.bed_type, in_queue,
        alloted,
        created_date
    ]

    if patient.patient_id in df_patient['patient_id'].unique():
        df_patient = df_patient.drop(
            index=df_patient[df_patient['patient_id'] == patient.patient_id].index).reset_index(drop=True)
    df_patient.loc[len(df_patient)] = data
    df_patient.to_csv("patient.csv", index=False)


async def log_json(request: Request):
    print(await request.json())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@api_router.post("/block_bed")
async def block_bed(
    patient: Patient,
    request: Request,
    username: str = Depends(get_current_username)

):
    # add patient to patient.csv

    alloted = False
    in_queue = True

    update_patient(alloted, in_queue, patient)
    update_data()

    return {"message": "bed blocked"}


@api_router.put("/allot_bed")
def allot_bed(
    patient: Patient,
    username: str = Depends(get_current_username)
):

    alloted = True
    in_queue = False

    update_patient(alloted, in_queue, patient)
    update_data()

    return {"message": "bed alloted"}


@api_router.put("/cured")
def becuredds(
    patient: Patient,
    username: str = Depends(get_current_username)
):

    alloted = False
    in_queue = False

    update_patient(alloted, in_queue, patient)
    update_data()

    return {"message": "bed cleared"}


@api_router.put("/deceased")
def deceased(
    patient: Patient,
    username: str = Depends(get_current_username)
):

    alloted = False
    in_queue = False

    update_patient(alloted, in_queue, patient)
    update_data()

    return {"message": "bed cleared"}


@api_router.get("/data")
def data(request: Request):
    # update_data()
    data = pd.read_csv("data.csv")

    data = data.groupby(['hospital', 'bed_type']).apply(
        lambda x: x[['total', 'occupied', 'vacant', 'queue']].to_dict('list')).reset_index()
    data_json = data.groupby('hospital').apply(lambda x: dict(
        zip(x['bed_type'], x[0]))).to_json(orient="index")
    data_json = json.loads(data_json)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "id": 123,
        "data": data_json
    })


@api_router.put("/update_data")
def update_data_api():
    update_data()
    return {"message": "data updated"}


app.include_router(api_router, dependencies=[Depends(log_json)])
