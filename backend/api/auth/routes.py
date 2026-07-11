from fastapi import APIRouter

from schemas.auth.request import RegisterRequest
from schemas.auth.response import RegisterResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/ping")
def auth_ping():
    return {"status": "ok", "module": "auth"}


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest):
    return RegisterResponse(message="Register endpoint scaffolded")