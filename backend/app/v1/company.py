from datetime import datetime
from fastapi import APIRouter,Request,Depends

from api.v1 import company_router as company_api
from db.session import get_db
from schemas.bill import BillShow
from  app.template import templates


router = APIRouter()

@router.get("/")
def home(request: Request, db=Depends(get_db)):
    companies =company_api.get_all_companies(db=db)
    context = {"request": request,"companies":companies}
    return templates.TemplateResponse("company/home.html",context)

@router.get("/party/{company_id}")
def company_detail(request: Request,company_id:int, db=Depends(get_db)):
    company =company_api.get_company(id=company_id, db=db)
    bills = [
        BillShow.model_validate(bill).model_dump()
        for bill in company.bills
    ]

    bills = sorted(bills, key=lambda bill: bill['bill_date'] or datetime.min)

    context = {"request": request,"company":company,"bills":bills}
    return templates.TemplateResponse("company/company_detail.html",context)



