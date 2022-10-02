from fastapi import APIRouter

from links.endpoints import router as links_router

router = APIRouter()
router.include_router(links_router)
