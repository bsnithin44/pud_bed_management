import secrets
import time

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import json
security = HTTPBasic()

router = APIRouter()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):

    # with open("co")
    with open("configs/config.json",'r') as f:
        config = json.load(f)

    correct_username = secrets.compare_digest(credentials.username, config['app_creds']['username'])
    correct_password = secrets.compare_digest(credentials.password, config['app_creds']['password'])
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

