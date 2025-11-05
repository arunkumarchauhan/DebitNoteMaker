from fastapi import APIRouter
from app.v1 import company
router = APIRouter()

router.include_router(company.router, prefix="/home",tags=[""],include_in_schema=False)
