from aiogram import Router

from .start import router as start_router
from .token import router as token_router

router = Router()
router.include_router(start_router)
router.include_router(token_router)