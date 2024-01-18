from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from src.model import Castle, CastleDistance, Distance, Restaurant
from src.schema import (
    ResponseCastle,
    ResponseCastleSimple,
    Restaurant as ResponseRestaurant
)
from src.google_api import fetch_route_api, fetch_route_api_during_castle
from fastapi import HTTPException

def fetch_castles(db: Session) -> List[Castle]:
    castles = db.query(Castle).all()
    res = []
    for castle in castles:
        res.append(ResponseCastleSimple(
            id=castle.id,
            name=castle.name,
            prefecture=castle.prefecture,
            address=castle.address
        ))
    return res

def fetch_specific_castles(db: Session, id: int) -> ResponseCastle:
    castle = db.query(Castle).filter_by(id=id).first()
    restaurants = fetch_restaurants(castle_id=id, db=db)
    return ResponseCastle(
        id=castle.id,
        name=castle.name,
        prefecture=castle.prefecture,
        lat=castle.lat,
        lng=castle.lng,
        holiday=castle.holiday,
        admission_time=castle.admission_time,
        admission_fee=castle.admission_fee,
        stamp=castle.stamp,
        restaurant=restaurants
    )

def fetch_restaurants(db: Session, castle_id: int) -> List[ResponseRestaurant]:
    res = []
    restaurants = db.query(Restaurant).filter_by(castle_id=castle_id).all()
    for restaurant in restaurants:
        res.append(ResponseRestaurant(
            name=restaurant.name,
            time=restaurant.time,
            holiday=restaurant.holiday,
            genre=restaurant.genre,
            url=restaurant.url
        ))
    return res

def fetch_travel(db: Session, arr: str, dep: str, castles: List[int]) -> Result:
    route = []
    
    distace: List[Distance] = []
    castle_info: List[Castle] = []
    # 城情報の取得
    for castle in castles:
        specific_castle = db.query(Castle).filter_by(id=castle).first()
        specific_castle_name = specific_castle.name
        if specific_castle_name is None:
            raise HTTPException(status_code=400, detail="Castle not found.")
        castle_info.append(specific_castle)
    first_route = fetch_route_api(origin=dep, dest=castle_info[0].address)
    distace.append(first_route)
    length = len(castles)
    if length >= 2:
        for i in range(1, length):
            route.append(db.query(CastleDistance).filter_by(castle_id_1=castles[i-1], castle_id_2=castles[i]).first())
            if route[i-1] == None:
                r = fetch_route_api_during_castle(origin=castle_info[i-1], dest=castle_info[i])
                route[i-1] = r.get("castle_distance")
                db.add(route[i-1])
                db.commit()
                distace.append(r.get("distance"))
            else:
                distace.append(Distance(
                    origin=castle_info[i-1].name,
                    dest=castle_info[i].name,
                    distance=route[i-1].distance,
                    time=route[i-1].time
                ))

    last_route = fetch_route_api(origin=castle_info[length-1].address, dest=arr)

    distace.append(last_route)
    
    return {
        "dep": dep,
        "arr": arr,
        "castles": [ResponseCastleSimple(id=d.id, name=d.name, prefecture=d.prefecture, address=d.address) for d in castle_info],
        "way_distance": [d.distance for d in distace],
        "way_time": [sec_to_str(d.time) for d in distace],
        "total_distance": sum([distace[i].distance for i in range(len(distace))]),
        "total_time": sec_to_str(sum([d.time for d in distace]))
    }

def sec_to_str(sec: int) -> str:
    day = sec // 86400
    hour = (sec % 86400) // 3600
    minute = (sec % 3600) // 60
    if day > 0: return f"{day}日{hour}時間{minute}分"
    else: return f"{hour}時間{minute}分"
