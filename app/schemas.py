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
    institute_name :str
    institute_type :str
    bed_type :str
    allotted : bool
    in_queue: bool
    created_date: str = None

    class Config:
        orm_mode = True

class InstituteBase(BaseModel):
    institute_type:str
    bed_type:str
    # state: Optional[str] =''
    total:int
    occupied:int
    vacant:int
    queue:int


class InstituteInDb(InstituteBase):
    institute_name:str
