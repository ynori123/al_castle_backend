from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from typing import List
from src.schema import (
    ResponseCastle,
    RequestCastle,
    ResponseCastleSimple,
    ResponseTravel,
    RequestTravel
)
from src.model import (
    Castle
)
from src.crud import (
    fetch_castles,
    fetch_specific_castles,
    fetch_travel
)
from src.database import get_db
from sqlalchemy.orm import Session
from src.auth import set_token, auth_token

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"ping" : "pong"}

@router.get("/castles", response_model=List[ResponseCastleSimple])
async def get_castles(db: Session = Depends(get_db)) -> List[Castle]:
    return fetch_castles(db=db)

@router.get("/castles/{id}", response_model=ResponseCastle)
async def get_castle(id: int, db: Session = Depends(get_db)) -> Castle:
    return fetch_specific_castles(id=id, db=db)

@router.post("/travel", response_model=ResponseTravel)
async def travel(data: RequestTravel, db: Session = Depends(get_db)):
    arr = data.arr
    dep = data.dep
    castles = data.castle
    token = data.token
    if auth_token(token=token):
        return fetch_travel(arr=arr, dep=dep, castles=castles, db=db)
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/token")
def get_token():
    token = set_token()
    return {"token": token}

@router.get("/auth")
def authenticate(token: str):
    result = auth_token(token=token)
    return {"result": result}
