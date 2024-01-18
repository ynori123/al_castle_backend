import requests
from src.config import setting
from src.model import Castle, CastleDistance, Distance
# from logging import getLogger

# logger = getLogger("uvicorn.app")
def fetch_route_api(origin: str, dest: str):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": dest,
        "key": setting.GOOGLE_MAP_API_KEY,
        "language": "ja",
    }
    # logger.info(params)
    req = requests.get(url, params=params)
    req_json = req.json()
    # logger.info(req_json)
    res = Distance(
        origin=origin,
        dest=dest,
        distance=req_json.get("rows")[0].get("elements")[0].get("distance").get("value") / 1000,
        time=req_json.get("rows")[0].get("elements")[0].get("duration").get("value")
    )
    return res

def fetch_route_api_during_castle(origin: Castle, dest: Castle):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin.address,
        "destinations": dest.address,
        "key": setting.GOOGLE_MAP_API_KEY,
        "language": "ja",
    }
    # logger.info(params)
    req = requests.get(url, params=params)
    req_json = req.json()
    res = Distance(
        origin=origin.name,
        dest=dest.name,
        distance=req_json.get("rows")[0].get("elements")[0].get("distance").get("value") / 1000,
        time=req_json.get("rows")[0].get("elements")[0].get("duration").get("value")
    )
    res_castle = CastleDistance(
        castle_id_1=origin.id,
        castle_id_2=dest.id,
        distance=req_json.get("rows")[0].get("elements")[0].get("distance").get("value") / 1000,
        time=req_json.get("rows")[0].get("elements")[0].get("duration").get("value")
    )
    return {"distance": res, "castle_distance": res_castle}
def search_castle_address(name: str):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": name,
        "language": "ja",
        "components": {"country":"JP"},
        "key": setting.GOOGLE_MAP_API_KEY,
    }
    req = requests.get(url, params=params)
    req_json = req.json()
    if req_json.get("status") != "OK":
        params = {
            "address": name+"跡",
            "language": "ja",
            "components": {"country":"JP"},
            "key": setting.GOOGLE_MAP_API_KEY,
        }
        req = requests.get(url, params=params)
        req_json = req.json()
        if req_json.get("status") != "OK":
            address = None
        else:
            address = req_json.get("results")[0].get("formatted_address")
    else:
        address = req_json.get("results")[0].get("formatted_address")
    return address
