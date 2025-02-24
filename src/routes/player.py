from fastapi import APIRouter, HTTPException
from starlette import status
import vlc
import time
from urllib.parse import unquote
from src.routes.memory import get_station, set_last_played, get_last_played

router = APIRouter(
    prefix="/player",
    tags=["Player"]
)

# Initialize VLC instance with specific options for Linux/Raspberry Pi
instance = vlc.Instance('--no-video')  # Audio only, no video output needed
player = instance.media_player_new()

async def play_radio(station_url: str):
    try:
        # Decode the URL properly
        decoded_url = unquote(station_url)
        media = instance.media_new(decoded_url)
        player.set_media(media)
        player.play()
        # Give VLC a moment to start playing and catch immediate errors
        time.sleep(1)
        if player.get_state() == vlc.State.Error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to play stream")
        return {"message": f"Now playing station: {decoded_url}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/status", status_code=status.HTTP_200_OK)
async def get_status():
    try:
        state = player.get_state()
        states = {
            vlc.State.NothingSpecial: "Idle",
            vlc.State.Opening: "Opening",
            vlc.State.Buffering: "Buffering",
            vlc.State.Playing: "Playing",
            vlc.State.Paused: "Paused",
            vlc.State.Stopped: "Stopped",
            vlc.State.Ended: "Ended",
            vlc.State.Error: "Error"
        }
        return {"status": states.get(state, "Unknown")}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/play/{station_id}", status_code=status.HTTP_200_OK)
async def play_station(station_id: int):
    station = await get_station(station_id)

    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    await set_last_played(station_id)
    await play_radio(station["url"])
    return {"message": f"Now playing station: {station['name']}"}


@router.post("/play_last_played", status_code=status.HTTP_200_OK)
async def play_last_played():
    last_played = await get_last_played()
    station = await get_station(last_played)
    await play_radio(station["url"])
    return {"message": f"Now playing station: {station['name']}"}
    

@router.get("/stop", status_code=status.HTTP_200_OK)
async def stop_radio():
    try:
        player.stop()
        return {"message": "Radio stopped"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))