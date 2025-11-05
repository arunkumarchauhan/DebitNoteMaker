from api.v1 import company_router,bill_router,transaction_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(company_router.router, prefix="/company", tags=["companies"])
router.include_router(bill_router.router, prefix="/bill", tags=["bills"])
router.include_router(transaction_router.router, prefix="/transaction", tags=["transactions"])
