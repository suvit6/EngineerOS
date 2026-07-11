from fastapi import APIRouter, HTTPException

from schemas.auth.request import RegisterRequest
from schemas.auth.response import RegisterResponse
from services.auth.service import create_user
from schemas.auth.request import LoginRequest
from schemas.auth.response import LoginResponse
from services.auth.service import authenticate_user
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/ping")
def auth_ping():
    return {"status": "ok", "module": "auth"}


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest):
  
    ok, message = create_user(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return RegisterResponse(message=message)

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    ok, message = authenticate_user(email=payload.email, password=payload.password)
    if not ok:
        raise HTTPException(status_code=401, detail=message)
    return LoginResponse(message=message)