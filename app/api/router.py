from fastapi.routing import APIRouter

from .auth import router as auth_router
from .users import router as user_router
from .tasks import router as tasks_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(tasks_router)
