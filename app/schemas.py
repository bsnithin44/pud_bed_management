from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    ticket_id: str
    patient_name: Optional[str] = None

class PatientUpdate(PatientBase):
    hospital: Optional[str] = ''
    ccc: Optional[str] =''
    bed_type: Optional[str] = 'no_bed_type'

class PatientCreate(PatientUpdate):
    allotted : bool
    in_queue: bool

class PatientInDb(PatientBase):
    patient_id : str
    institute :str
    institute_type :str
    bed_type :str
    allotted : bool
    in_queue: bool
    created_date: str = None

    class Config:
        orm_mode = True

class HospitalBase(BaseModel):
    institute:str
    institute_type:str
    # state: Optional[str] =''

class HospitalCreate(HospitalBase):
    bed_type:str
    total:int
    occupied:int
    vacant:int
    queue:int

class HospitalUpdate(HospitalBase):
    bed_type:str
    total:int
    occupied:int
    vacant:int
    queue:int

