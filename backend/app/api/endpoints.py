from fastapi import APIRouter
from app.api.routes import users, addresses, plans, addons, support, usage

router = APIRouter()

# Include all route modules
router.include_router(users.router)
router.include_router(addresses.router)
router.include_router(plans.router)
router.include_router(addons.router)
router.include_router(support.router)
router.include_router(usage.router)