from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime
import pandas as pd

def get_patient(db: Session, patient_id: str ):
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()

def get_patient_derived_feilds(patient:schemas.PatientCreate):

    if patient.bed_type == '':
        bed_type = 'no_bed_type'
    else:
        bed_type = patient.bed_type    
    institute_flag = 0
    if len(patient.hospital)>1:
        institute = patient.hospital
        institute_flag = 1
        institute_type = 'hospital'

    elif len(patient.ccc)>1:
        institute = patient.ccc
        institute_flag = 1
        institute_type = 'ccc'
    else:
        institute = 'none'
        institute_type = 'none'
        institute_flag = 0

    return bed_type,institute_type,institute, institute_flag

def create_patient(db: Session, patient: schemas.PatientCreate, allotted, in_queue):

    bed_type, institute_type, institute, institute_flag = get_patient_derived_feilds(patient)
    
    if institute_flag:
        db_patient = models.Patient(
            patient_id = patient.patient_id,
            ticket_id = patient.ticket_id, 
            institute = institute,
            institute_type = institute_type,
            bed_type = bed_type,
            allotted = allotted,
            in_queue = in_queue,
            created_date = datetime.now()
            )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return 1, db_patient
    else:
        return 0, None


def update_patient(db: Session, patient: schemas.PatientCreate, allotted, in_queue):

    bed_type, institute_type, institute, institute_flag = get_patient_derived_feilds(patient)

    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient.patient_id).first()
    if institute_flag:

        db_patient.bed_type = bed_type
        db_patient.institute = institute
        db_patient.institute_type = institute_type

        db_patient.allotted = allotted
        db_patient.in_queue = in_queue
        db_patient.created_date = datetime.now()

        db.commit()
        db.refresh(db_patient)
        return 1, db_patient
    else:
        return 0, None

def initialise_data_in_db(db:Session):
    df = pd.read_csv("data.csv")
    df['id'] = df.index.astype(int)
    df.to_sql(name='institute_master', con=db.bind, index=False,if_exists='replace')

def update_data(db:Session):
    df_data = pd.read_sql("institute_master",con=db.bind)
    df_patient = pd.read_sql("patients",con = db.bind)

    df_patient['patient_id'] = df_patient['patient_id'].astype(str)

    for institute in df_data.institute.unique():
        df_p1 = df_patient[df_patient['institute'] == institute]

        for bed_type in ('Oxygen Bed', 'Isolation Bed', 'Ventilator Bed'):
            df_p1_b = df_p1[df_p1['bed_type'] == bed_type]
            index_ = df_data[(df_data['institute'] == institute) & (
                df_data['bed_type'] == bed_type)].index

            occupied = df_p1_b[df_p1_b['allotted']
                               == True]['patient_id'].count()
            queue = df_p1_b[df_p1_b['in_queue'] == True]['patient_id'].count()
            total = df_data.iloc[index_]['total']
            vacant = total - occupied
            df_data.loc[index_, ('occupied', 'vacant', 'queue')] = [
                occupied, vacant, queue]

        df_p1_q = df_p1[df_p1['in_queue'] == True]
        queue_not_decided = df_p1_q[(
            df_p1_q['bed_type'] == 'no_bed_type') |(df_p1_q['bed_type'] == '')]['patient_id'].count()
        df_data.loc[(df_data['institute'] == institute) & (
            df_data['bed_type'] == 'no_bed_type'), 'queue'] = queue_not_decided
    df_data.to_sql(name='institute_master', con=db.bind, index=False,if_exists='replace')
