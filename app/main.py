import json

import pandas as pd
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app import auth, crud, models, schemas
from app.api.v1 import beds, patients, institutes
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
api_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(
    router=auth.router,
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[Depends(dependency=auth.get_current_username)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    router=patients.router,
    prefix="/api/v1",
    tags=["Patients v1"],
    dependencies=[Depends(dependency=auth.get_current_username)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    router=institutes.router,
    prefix="/api/v1",
    tags=["Institutes v1"],
    dependencies=[Depends(dependency=auth.get_current_username)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    router=beds.router,
    prefix="/api/v1",
    tags=["Beds"],
    # dependencies=[Depends()],
    responses={404: {"description": "Not found"}},
)

async def log_json(request: Request):
    print(await request.json())

@app.on_event("startup")
def startup_event():
    print('Initialising db')
    db = SessionLocal()
    crud.initialise_data_in_db(db, filename = "data.csv")
    db.close()

@app.get(
    "/dashboard/institutes", 
    status_code=status.HTTP_200_OK,
)
async def read_institutes(
    request: Request,
    db: Session = Depends(get_db),
    # username: str = Depends(auth.get_current_username)
):
    data = pd.read_sql("institutes",con=db.bind)

    hospital = data[data['institute_type']=='hospital']
    hospital = hospital.groupby(['institute_name', 'bed_type']).apply(
        lambda x: x[['total', 'occupied', 'vacant', 'queue']].to_dict('list')).reset_index()
    hospital_json = hospital.groupby('institute_name').apply(lambda x: dict(
        zip(x['bed_type'], x[0]))).to_json(orient="index")
    hospital_json = json.loads(hospital_json)


    ccc = data[data['institute_type']=='ccc']

    ccc = ccc.groupby(['institute_name', 'bed_type']).apply(
        lambda x: x[['total', 'occupied', 'vacant', 'queue']].to_dict('list')).reset_index()
    ccc_json = ccc.groupby('institute_name').apply(lambda x: dict(
        zip(x['bed_type'], x[0]))).to_json(orient="index")
    ccc_json = json.loads(ccc_json)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "hospital_json": hospital_json,
        "ccc_json": ccc_json
    })
app.include_router(api_router, dependencies=[Depends(log_json)])
