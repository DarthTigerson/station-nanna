from fastapi import APIRouter, HTTPException
from starlette import status
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

@router.get("/stations", status_code=status.HTTP_200_OK)
async def get_stations():
    data = read_data()
    return data["stations"]

@router.get("/stations/{station_id}", status_code=status.HTTP_200_OK)
async def get_station(station_id: int):
    data = read_data()
    station = next((s for s in data["stations"] if s["id"] == station_id), None)
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return station

@router.patch("/last-played/{station_id}", status_code=status.HTTP_200_OK)
async def set_last_played(station_id: int):
    data = read_data()
    data["last_played"] = station_id
    with open("src/data.json", "w") as f:
        json.dump(data, f)
    return {"message": "Last played station updated"}

@router.get("/last-played", status_code=status.HTTP_200_OK)
async def get_last_played():
    data = read_data()
    
    if data["last_played"] is None:
        raise HTTPException(status_code=404, detail="No station played yet")
    
    return await get_station(data["last_played"])

@router.get("/wifi", status_code=status.HTTP_200_OK)
async def get_wifi():
    data = read_data()
    
    if not data["wifi"]:
        raise HTTPException(status_code=404, detail="No wifi credentials found")
    
    wifi = data["wifi"][0]  # Get the first (and only) wifi config
    
    if wifi["ssid"] == 'SSID' or wifi["password"] == 'PASSWORD':
        raise HTTPException(status_code=404, detail="Default credentials found, please set your own")
    
    return wifi
