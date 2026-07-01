from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_uc, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(
    data: RegisterRequest,
    uc: AuthUseCase = Depends(get_auth_uc),
):
    token = await uc.register(data.email, data.password)
    return TokenResponse(access_token=token, token_type="bearer")


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    uc: AuthUseCase = Depends(get_auth_uc),
):
    token = await uc.login(form.username, form.password)
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/me")
async def me(user=Depends(get_current_user)):
    return user