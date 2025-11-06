from fastapi import APIRouter
from app.v1 import company
from app.v1 import bills
router = APIRouter()

router.include_router(company.router, prefix="",tags=[""],include_in_schema=False)
router.include_router(bills.router, prefix="/party",tags=[""],include_in_schema=False)
