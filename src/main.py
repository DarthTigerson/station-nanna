from fastapi import FastAPI
from src.routes import player, testing

app = FastAPI()

app.include_router(player.router)
app.include_router(testing.router)
