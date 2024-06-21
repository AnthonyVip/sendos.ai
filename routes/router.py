from fastapi import APIRouter
from routes.api.router import router as api_router
from routes.auth.router import router as users_router

router = APIRouter()
router.include_router(api_router, prefix="", tags=["api"])
router.include_router(users_router, prefix="/users", tags=["users"])
