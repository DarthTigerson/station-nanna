from fastapi import APIRouter
import vlc
from fastapi.responses import JSONResponse
import time
from urllib.parse import unquote


router = APIRouter(
    prefix="/player",
    tags=["Player"]
)

# Initialize VLC instance with specific options for Linux/Raspberry Pi
instance = vlc.Instance('--no-video')  # Audio only, no video output needed
player = instance.media_player_new()

@router.post("/play/{station_url:path}")
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
            raise Exception("Failed to play stream")
        return JSONResponse(
            content={"message": f"Now playing station: {decoded_url}"},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )

@router.get("/stop")
async def stop_radio():
    try:
        player.stop()
        return JSONResponse(
            content={"message": "Radio stopped"},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )

@router.get("/status")
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
        return JSONResponse(
            content={"status": states.get(state, "Unknown")},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )
