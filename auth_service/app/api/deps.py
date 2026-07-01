from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.core.security import decode_token
from app.repositories.users import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# DB SESSION
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# REPOSITORY
def get_users_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


# USECASE
def get_auth_uc(repo=Depends(get_users_repo)):
    from app.usecases.auth import AuthUseCase
    return AuthUseCase(repo)


# JWT -> user_id
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_token(token)
        return int(payload["sub"])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# USER FROM DB
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    repo: UserRepository = Depends(get_users_repo),
):
    user = await repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user