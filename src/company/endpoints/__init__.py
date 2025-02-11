from company.endpoints.division import router as division_router
from company.endpoints.employee import router as employee_router
from company.endpoints.position import router as position_router
from company.endpoints.status import router as status_router

__all__ = [
    "division_router",
    "employee_router",
    "position_router",
    "status_router"
]
