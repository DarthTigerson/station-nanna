from fastapi import APIRouter
import json
from pathlib import Path


router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)



def read_data():
    data_file = Path("src/data.json")
    with open(data_file, "r") as f:
        return json.load(f)

@router.get("/stations")
async def get_stations():
    data = read_data()
    return data["stations"]

@router.get("/stations/{station_id}")
async def get_station(station_id: int):
    data = read_data()
    station = next((s for s in data["stations"] if s["id"] == station_id), None)
    if station is None:
        return {"error": "Station not found"}, 404
    return station

@router.patch("/last-played/{station_id}")
async def set_last_played(station_id: int):
    data = read_data()
    data["last_played"] = station_id
    with open("src/data.json", "w") as f:
        json.dump(data, f)
    return {"message": "Last played station updated"}, 200

@router.get("/last-played")
async def get_last_played():
    data = read_data()
    return await get_station(data["last_played"])
