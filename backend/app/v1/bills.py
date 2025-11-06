from fastapi import APIRouter, Depends, HTTPException, Request
from db.repository import bill as bill_repo
from db.session import get_db
from schemas.bill import BillShow
from app.template import templates
from datetime import timedelta,datetime

router = APIRouter()


@router.get("/bill/{bill_number}")
def bill_list(request: Request,bill_number: int, db=Depends(get_db)):
    bill = bill_repo.get_bill_by_bill_number(bill_number=bill_number, db=db)
    
    return templates.TemplateResponse("bill/bill_summary.html", {"request": request, "bill": bill,"today":datetime.now()})
