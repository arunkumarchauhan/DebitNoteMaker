from fastapi import APIRouter, Depends, HTTPException
from db.repository import bill as bill_repo
from db.session import get_db
from schemas.bill import BillShow
router = APIRouter()


@router.get("/bill/{bill_number}")
def bill_list(bill_number: int, db=Depends(get_db)):
    bill = bill_repo.get_bill_by_bill_number(bill_number=bill_number, db=db)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return BillShow.model_validate(bill)
