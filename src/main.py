from fastapi import FastAPI
from src.routes import controls, memory, player

app = FastAPI()

app.include_router(controls.router)
app.include_router(memory.router)
app.include_router(player.router)
