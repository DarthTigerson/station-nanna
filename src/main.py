from fastapi import FastAPI
from src.routes import controls, memory, player

app = FastAPI(
    title="Station Nanna",
    description="Nanna's radio station",
    version="0.1.0"
)

app.include_router(controls.router)
app.include_router(memory.router)
app.include_router(player.router)