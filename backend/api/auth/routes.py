from fastapi import APIRouter, HTTPException

from schemas.auth.request import RegisterRequest
from schemas.auth.response import RegisterResponse
from services.auth.service import create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/ping")
def auth_ping():
    return {"status": "ok", "module": "auth"}


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest):
    fake_hash = f"plain::{payload.password}"
    ok, message = create_user(
        email=payload.email,
        password_hash=fake_hash,
        full_name=payload.full_name,
    )
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return RegisterResponse(message=message)