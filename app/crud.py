from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime
import pandas as pd
from typing import List

# institutes
def get_institutes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Institute).offset(skip).limit(limit).all()



def create_institutes(db: Session, institutes: List[schemas.InstituteInDb] ):
    num_of_deleted_rows = db.query(models.Institute).delete()

    for institute in institutes:
        print()
        try:
            institute = models.Institute(**institute.dict())
            db.add(institute)
        except:
            pass

    db.commit()
    return db.query(models.Institute).count()


def update_institutes(db: Session, institutes: List[schemas.InstituteInDb] ):
    
    for institute in institutes:
        institute = models.Institute(**institute.dict())


        db_institute = db.query(models.Institute)\
        .filter(models.Institute.institute_name == institute.institute_name,
        models.Institute.institute_type == institute.institute_type,
        models.Institute.bed_type == institute.bed_type).first()


        if db_institute:
            
            db_institute.total = institute.total
            db_institute.occupied = institute.occupied
            db_institute.vacant = institute.vacant
            db_institute.queue = institute.total
        else:
            db.add(institute)

    db.commit()
    return db.query(models.Institute).count()

def delete_institutes(db: Session):
    deleted_rows = db.query(models.Institute).delete()
    db.commit()
    return deleted_rows

# patients
def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def create_patients(db: Session, patients: List[schemas.PatientInDb] ):
    num_of_deleted_rows = db.query(models.Patient).delete()

    for patient in patients:
        try:
            patient = models.Patient(**patient.dict())
            db.add(patient)
        except:
            pass

    db.commit()
    return db.query(models.Patient).count()

def update_patients(db: Session, patients: List[schemas.PatientInDb] ):
    
    for patient in patients:
        patient = models.Patient(**patient.dict())
        db_patient = get_patient_by_id(db, patient.patient_id)
        if db_patient:
            flag = delete_patient_by_id(db,patient.patient_id)
        else:
            pass
        db.add(patient)

    db.commit()
    return db.query(models.Patient).count()

def delete_patients(db: Session):
    deleted_rows = db.query(models.Patient).delete()
    db.commit()
    return deleted_rows

# patiend by id

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

def create_patient_by_id(db: Session, patient: schemas.PatientCreate, patient_id: str):
    bed_type, institute_type, institute, institute_flag = get_patient_derived_feilds(patient)
    
    if institute_flag:
        db_patient = models.Patient(
            patient_id = patient_id,
            ticket_id = patient.ticket_id, 
            institute = institute,
            institute_type = institute_type,
            bed_type = bed_type,
            allotted = patient.allotted,
            in_queue = patient.in_queue,
            created_date = datetime.now()
            )
        db.add(db_patient)
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


def get_patient_by_id(db: Session, patient_id: str ):
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()

def delete_patient_by_id(db: Session, patient_id: str ):
    db.query(models.Patient).filter(models.Patient.patient_id == patient_id).delete()
    db.commit()
    return 1

def update_patient_by_id(db: Session, patient: schemas.PatientCreate, patient_id :str):

    bed_type, institute_type, institute, institute_flag = get_patient_derived_feilds(patient)

    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if institute_flag:

        db_patient.bed_type = bed_type
        db_patient.institute = institute
        db_patient.institute_type = institute_type

        db_patient.allotted = db_patient.allotted
        db_patient.in_queue = db_patient.in_queue
        db_patient.created_date = datetime.now()

        db.commit()
        db.refresh(db_patient)
        return 1, db_patient
    else:
        return 0, None