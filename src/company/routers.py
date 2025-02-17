from fastapi import APIRouter

from company.endpoints import (
    division_router,
    employee_router,
    position_router,
    status_router,
)

router = APIRouter()

router.include_router(division_router, prefix="/division", tags=("Division",))
router.include_router(position_router, prefix="/position", tags=("Position",))
router.include_router(status_router, prefix="/status", tags=("Status",))
router.include_router(employee_router, prefix="/employee", tags=("Employee",))
