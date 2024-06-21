from fastapi import APIRouter
from routes.api.router import router as api_router

router = APIRouter()
router.include_router(api_router, prefix="/api", tags=["api"])