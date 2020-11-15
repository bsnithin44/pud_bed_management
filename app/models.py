from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String, unique=True, primary_key=True, index=True)
    patient_name = Column(String, unique=False, default = None)

    ticket_id = Column(String, unique=True, index=True)

    institute = Column(String, unique=False, index=True,default = '')
    institute_type = Column(String, unique=False, index=True,default= '')

    bed_type = Column(String, unique=False, index=True,default= 'no_bed_type')
    allotted = Column(Boolean, default=False)
    in_queue = Column(Boolean, default=False)
    created_date = Column(String, unique=False, index=True,default= '')

class InstituteData(Base):
    __tablename__ = "institute_master"

    id = Column(String, unique=True, primary_key = True, index=True)
    institute_type = Column(String, unique=False, index=True)
    institute = Column(String, unique=False, index=True)
    bed_type = Column(String, unique=False, index=True)
    total = Column(Float, unique=False, index=False)
    occupied = Column(Float, unique=False, index=False)
    vacant = Column(Float, unique=False, index=False)
    queue = Column(Float, unique=False, index=False)


    
