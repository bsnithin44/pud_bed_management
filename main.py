import secrets
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
import json
app = FastAPI()

security = HTTPBasic()
username = 'nithin'
password = "nithintest"


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest( credentials.password, password)
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

    for hospital in df_data.hospital_name.unique():
        
        
        df_p1 = df_patient[df_patient['hospital_name'] == hospital]
        df_p1_q = df_p1[df_p1['in_queue']==True]

        queue_not_decided = df_p1_q[(df_p1_q['bed_type']=='no_bed_type')]['patient_id'].count()
        queue_oxygen = df_p1_q[(df_p1_q['bed_type']=='Oxygen Bed')]['patient_id'].count()
        queue_isolation =df_p1_q[(df_p1_q['bed_type']=='Isolation Bed')]['patient_id'].count()
        queue_ventilator = df_p1_q[(df_p1_q['bed_type']=='Ventilator Bed')]['patient_id'].count()
        
        df_p1_a = df_p1[df_p1['alloted']==True]
        alloted_oxygen = df_p1_a[(df_p1_a['bed_type']=='Oxygen Bed')]['patient_id'].count()
        alloted_isolation =df_p1_a[(df_p1_a['bed_type']=='Isolation Bed')]['patient_id'].count()
        alloted_ventilator = df_p1_a[(df_p1_a['bed_type']=='Ventilator Bed')]['patient_id'].count()

        index_ = df_data[df_data['hospital_name']==hospital].index
        print(index_)
        print(alloted_isolation, alloted_oxygen, alloted_ventilator,
            queue_isolation, queue_oxygen, queue_ventilator,
            queue_not_decided)
        df_data.loc[index_,('alloted_isolation_beds','alloted_oxygen_beds','alloted_ventilator_beds',
            'queue_isolation_beds','queue_oxygen_beds','queue_ventilator_beds',
            'queue_not_decided')] = [
            alloted_isolation, alloted_oxygen, alloted_ventilator,
            queue_isolation, queue_oxygen, queue_ventilator,
            queue_not_decided

        ]
        df_data.to_csv("data.csv",index=False)

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/block_bed")
def block_bed(
    patient : Patient,
    username: str = Depends(get_current_username),
    ):
    # add patient to patient.csv
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_patient = pd.read_csv("patient.csv")
    df_patient['patient_id'] = df_patient['patient_id'].astype(str)

    alloted = False
    in_queue = True
    data = [
        patient.patient_id, patient.ticket_id, patient.hospital,
        patient.name, patient.bed_type, in_queue,
        alloted,
        created_date
    ]

    if patient.patient_id in df_patient['patient_id'].unique():
        df_patient = df_patient.drop(index=df_patient[df_patient['patient_id']==patient.patient_id].index).reset_index(drop=True)
    df_patient.loc[len(df_patient)] = data
    df_patient.to_csv("patient.csv",index=False)


    df_patient.to_csv("patient.csv",index=False)
    update_data()
    return {"message": "bed blocked"}


@app.put("/allot_bed")
def allot_bed(
    patient : Patient,
    username: str = Depends(get_current_username)
    ):

    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_patient = pd.read_csv("patient.csv")
    df_patient['patient_id'] = df_patient['patient_id'].astype(str)

    alloted = True
    in_queue = False
    data = [
        patient.patient_id, patient.ticket_id, patient.hospital,
        patient.name, patient.bed_type, in_queue,
        alloted,
        created_date
    ]
    if patient.patient_id in df_patient['patient_id'].unique():
        df_patient = df_patient.drop(index=df_patient[df_patient['patient_id']==patient.patient_id].index).reset_index(drop=True)
    df_patient.loc[len(df_patient)] = data
    df_patient.to_csv("patient.csv",index=False)

    update_data()
    return {"message": "bed alloted"}

@app.put("/cured")
def becuredds(
    patient : Patient,
    username: str = Depends(get_current_username)
    ):

    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_patient = pd.read_csv("patient.csv")
    df_patient['patient_id'] = df_patient['patient_id'].astype(str)

    alloted = False
    in_queue = False
    data = [
        patient.patient_id, patient.ticket_id, patient.hospital,
        patient.name, patient.bed_type, in_queue,
        alloted,
        created_date
    ]
    if patient.patient_id in df_patient['patient_id'].unique():
        df_patient = df_patient.drop(index=df_patient[df_patient['patient_id']==patient.patient_id].index).reset_index(drop=True)
    df_patient.loc[len(df_patient)] = data
    df_patient.to_csv("patient.csv",index=False)

    update_data()
    return {"message": "bed cleared"}

@app.put("/deceased")
def deceased(
    patient : Patient,
    username: str = Depends(get_current_username)
    ):

    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_patient = pd.read_csv("patient.csv")
    df_patient['patient_id'] = df_patient['patient_id'].astype(str)

    alloted = False
    in_queue = False
    data = [
        patient.patient_id, patient.ticket_id, patient.hospital,
        patient.name, patient.bed_type, in_queue,
        alloted,
        created_date
    ]
    if patient.patient_id in df_patient['patient_id'].unique():
        df_patient = df_patient.drop(index=df_patient[df_patient['patient_id']==patient.patient_id].index).reset_index(drop=True)
    df_patient.loc[len(df_patient)] = data
    df_patient.to_csv("patient.csv",index=False)

    update_data()
    return {"message": "bed cleared"}

@app.get("/data")
def data():
    data = pd.read_csv("data.csv")
    data = data.groupby("hospital_name").sum()
    data_json = data.to_json()
    data_json = json.loads(data_json)
    return data_json