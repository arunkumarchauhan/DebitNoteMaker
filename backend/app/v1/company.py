from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from db.repository import company as company_repository
from api.v1 import company_router as company_api
from db.session import get_db
templates = Jinja2Templates(directory="template")


router = APIRouter()

@router.get("")
def home(request: Request, db=Depends(get_db)):
    companies =company_api.get_all_companies(db=db)
    context = {"request": request,"companies":companies}
    return templates.TemplateResponse("company/home.html",context)

@router.get("/{company_id}")
def company_detail(request: Request,company_id:int, db=Depends(get_db)):
    company =company_api.get_company(id=company_id, db=db)
    bills = company.bills
    context = {"request": request,"company":company,"bills":bills}
    return templates.TemplateResponse("company/company_detail.html",context)


