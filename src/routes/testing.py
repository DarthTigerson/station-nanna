from fastapi import APIRouter


router = APIRouter(
    prefix="/testing",
    tags=["Testing"]
)

@router.get("/")
async def testing():
    return {"message": "Hello, World!"}
