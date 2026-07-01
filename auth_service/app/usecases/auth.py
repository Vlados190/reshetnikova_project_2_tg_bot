from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.repositories.users import UserRepository
from app.db.models import User
from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)


class AuthUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, email: str, password: str) -> str:
        existing = await self.repo.get_by_email(email)

        if existing:
            raise UserAlreadyExistsError()

        user = User(
            email=email,
            password_hash=hash_password(password),
            role="user",
        )

        user = await self.repo.create(user)

        token = create_access_token(
            user_id=user.id,
            role=user.role,
        )

        return token

    async def login(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        token = create_access_token(
            user_id=user.id,
            role=user.role,
        )

        return token

    async def me(self, user_id: int):
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError()

        return user