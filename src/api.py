from fastapi import APIRouter

from company import router as company_router

main_api_v1_router = APIRouter()
main_api_v1_router.include_router(
    company_router, prefix="/company", tags=("Company",)
)
