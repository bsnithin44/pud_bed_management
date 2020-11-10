from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    ticket_id: str
    patient_id: str
    hospital: Optional[str] = ''
    ccc: Optional[str] =''
    bed_type: Optional[str] = 'no_bed_type'
    name: Optional[str] = None

class PatientCreate(PatientBase):
    alloted : bool = False
    in_queue: bool = False
    created_date: str = None