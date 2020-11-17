from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.database import Base

class Institute(Base):
    __tablename__='institutes'

    institute_name = Column(String, unique=True, primary_key=True, index=True)
    institute_type = Column(String, index=True)
    bed_type = Column(String, index=True)
    total = Column(Integer)
    occupied = Column(Integer,default =0)
    vacant = Column(Integer)
    queue = Column(Integer,default=0)


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

    # def __init__(self, data):
    #     for d in data:
    #         print(d[0],d[1])
    #         # self.d[0] = d[1] 
    #     # self.patient_id=patient_id
    #     # self.patient_name=patient_name
    #     # self.ticket_id=ticket_id
    #     # self.institute=institute
    #     # self.institute_type=institute_type
    #     # self.bed_type=bed_type
    #     # self.allotted=allotted
    #     # self.in_queue=in_queue
    #     # self.created_date=created_date

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


    
