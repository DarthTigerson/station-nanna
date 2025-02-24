from fastapi import APIRouter, HTTPException
from starlette import status
from src.routes.memory import get_station, set_last_played, get_last_played
from src.routes.player import play_radio


router = APIRouter(
    prefix="/controls",
    tags=["Controls"]
)

@router.post("/play/{station_id}", status_code=status.HTTP_200_OK)
async def play_station(station_id: int):
    station = await get_station(station_id)

    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    await set_last_played(station_id)
    await play_radio(station["url"])

@router.post("/play_last_played", status_code=status.HTTP_200_OK)
async def play_last_played():
    last_played = await get_last_played()
    await play_radio(last_played["url"])
