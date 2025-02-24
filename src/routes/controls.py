from fastapi import APIRouter, HTTPException
from starlette import status
from src.routes.memory import get_wifi
import os

router = APIRouter(
    prefix="/controls",
    tags=["Controls"]
)

@router.get("/connect_to_wifi", status_code=status.HTTP_200_OK)
async def connect_to_wifi():
    await deactivate_hotspot()
    wifi = await get_wifi()
    
    if wifi is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No wifi credentials found")
    
    try:    
        wifi_status =   os.system(f"nmcli dev wifi connect {wifi['ssid']} password {wifi['password']}")
        
        if wifi_status != 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to connect to wifi")
        
        return {"message": f"Pi connected to wifi {wifi['ssid']}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/activate_hotspot", status_code=status.HTTP_200_OK)
async def activate_hotspot():
    try:
        # Stop the NetworkManager service to prevent interference
        os.system("sudo systemctl stop NetworkManager")
        
        # Configure the wireless interface as an access point
        os.system("sudo nmcli device wifi hotspot ifname wlan0 ssid station-nanna")
        
        # Start NetworkManager again
        os.system("sudo systemctl start NetworkManager")
        
        return {"message": "Hotspot created successfully with SSID: station-nanna"}
    except Exception as e:
        # Ensure NetworkManager is restarted even if there's an error
        os.system("sudo systemctl start NetworkManager")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/deactivate_hotspot", status_code=status.HTTP_200_OK)
async def deactivate_hotspot():
    try:
        # Stop the hotspot by restarting NetworkManager
        os.system("sudo systemctl restart NetworkManager")
            
        return {"message": f"Hotspot deactivated"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))