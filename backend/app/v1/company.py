from datetime import datetime
from fastapi import APIRouter,Request,Depends

from api.v1 import company_router as company_api
from db.session import get_db
from schemas.bill import BillShow
from  app.template import templates
from db.models.company import Company
from db.models.bill import Bill
from schemas.company import CompanyShow
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
    
    context = {"request": request,"company":company,"bills":company.bills}
    return templates.TemplateResponse("company/company_detail.html",context)

def create_transactions_for_company(company:Company,roi:float):
    all_transactions_df = []
    for bill in company.bills:
        bill_transactions_df=create_transaction(bill,roi)
        all_transactions_df=all_transactions_df+bill_transactions_df
    return all_transactions_df

def create_transaction(bill:Bill,roi:float):
    df = []
    pending_amount=bill.amount
    isFirstTransaction=True
    for transaction in bill.transactions:
        pending_amount=pending_amount - transaction.amount_paid  
        
        new_row_df=create_transaction_entry(bill_id=bill.id,
                               roi=roi,
                               bank_transaction_id=transaction.bank_transaction_id,
                               payment_mode=transaction.payment_mode,
                               due_date=bill.due_date,
                                payment_date=transaction.payment_date,
                                bill_amount=bill.amount if isFirstTransaction else None, 
                                amount_paid=transaction.amount_paid,
                                pending_amount=pending_amount,
                                description=transaction.description)    
        df.append(new_row_df)
        isFirstTransaction=False

    if pending_amount>0:
        new_row_df=create_transaction_entry(bill_id=bill.id,
                                roi=roi,
                                bank_transaction_id=None,
                                payment_mode=None,
                                due_date=bill.due_date,
                                payment_date=datetime.now(),
                                bill_amount=bill.amount, 
                                amount_paid=0.0,
                                pending_amount=pending_amount,
                                description="No payment made yet")    
        df.append(new_row_df)

    return df
             

def create_transaction_entry(bill_id:int,roi:float, bank_transaction_id:str|None,payment_mode:str|None,due_date:datetime, payment_date:datetime|None, bill_amount:float|None,  amount_paid:float,pending_amount:float,description:str):
    delayed_days = (payment_date - due_date).days 
    if delayed_days < 0:
            delayed_days = 0
    penalty=amount_paid*(roi/100)*(delayed_days/30)
    if amount_paid==0 and delayed_days>0:
        penalty=pending_amount*(roi/100)*(delayed_days/30)
        
    data = {
            "bill_id": bill_id,
            "transaction_id": bank_transaction_id,
            "payment_mode":payment_mode,
            "due_date": due_date,
            "payment_date": payment_date,
            "bill_amount":  bill_amount,
            "amount_paid": amount_paid,
            "delayed_days": delayed_days,
            "pending_amount": pending_amount,
            "penalty":penalty,
            "description": description,
        }  
   
    return data



@router.get("/bills-by/{company_id}")
def bills_by_company_id(request: Request,company_id:int, db=Depends(get_db)):
    company =company_api.get_company(id=company_id, db=db)
    transactions_df=create_transactions_for_company(company=company,roi=2)
   
    total_penalty=sum([tx["penalty"] for tx in transactions_df])
    total_pending=sum([tx["pending_amount"] for tx in transactions_df])
    context = {"company":CompanyShow.model_validate(company),"bill":{
        "transactions":transactions_df,
        "total_penalty":total_penalty,
        "pending_amount":total_pending,
        "total_amount":total_penalty+total_pending    
     }}
    return context

@router.get("/company-transaction/{company_id}")
def company_transaction(request: Request,company_id:int, db=Depends(get_db)):
    company =company_api.get_company(id=company_id, db=db)
    transactions_df=create_transactions_for_company(company=company,roi=2)
   
    total_penalty=sum([tx["penalty"] for tx in transactions_df])
    total_pending=sum([tx["pending_amount"] for tx in transactions_df])
    context = {"request": request,
        "company":CompanyShow.model_validate(company),
        "bill":{
        "transactions":transactions_df,
        "total_penalty":total_penalty,
        "pending_amount":total_pending,
        "total_amount":total_penalty+total_pending    ,
        "interest":2
     }}
    return templates.TemplateResponse("company/company_transactions.html",context)