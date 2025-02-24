from fastapi import APIRouter, HTTPException
from starlette import status
import requests
import os

router = APIRouter(
    prefix="/error_handling",
    tags=["Error Handling"]
)

@router.get("/check_internet", status_code=status.HTTP_200_OK)
async def check_internet():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        response.raise_for_status()
        return {"message": "Internet connection is active"}
    except requests.RequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    
@router.get("/check_wifi", status_code=status.HTTP_200_OK)
async def check_wifi():
    try:
        os.system("nmcli dev wifi")
        return {"message": "Wifi connection is active"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/validate_station_url", status_code=status.HTTP_200_OK)
async def validate_station_url(station_url: str):
    try:
        response = requests.get(station_url, timeout=5)
        response.raise_for_status()
        return {"message": "Station URL is valid"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))