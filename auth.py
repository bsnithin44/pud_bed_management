import secrets
import time

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from mysecrets import username,password

security = HTTPBasic()


class Service(BaseModel):
    service_id: str
    service_name: str
    run_id: str

router = APIRouter()


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



@router.get("/status", status_code=status.HTTP_200_OK)
def status_check():
    return "Auth is active"

