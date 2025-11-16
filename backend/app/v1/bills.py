from fastapi import APIRouter, Depends, HTTPException, Request
from db.repository import bill as bill_repo
from db.session import get_db
from schemas.bill import BillShow
from app.template import templates
from datetime import timedelta,datetime
from db.models.company import Company
from db.models.bill import Bill
from api.v1 import company_router as company_api
from schemas.company import CompanyShow
import pandas as pd
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter()


@router.get("/bill/{bill_number}")
def bill_list(request: Request,bill_number: int, db=Depends(get_db)):
    bill = bill_repo.get_bill_by_bill_number(bill_number=bill_number, db=db)
    
    return templates.TemplateResponse("bill/bill_summary.html", {"request": request, "bill": bill,"today":datetime.now()})

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
        
        new_row_df=create_transaction_entry(id=transaction.id,
                               bill_id=bill.id,
                               bill_number=bill.bill_number,
                               roi=roi,
                               bank_transaction_id=transaction.bank_transaction_id,
                               payment_mode=transaction.payment_mode,
                               bill_date=bill.bill_date,
                               due_date=bill.due_date,
                                payment_date=transaction.payment_date,
                                bill_amount=bill.amount if isFirstTransaction else None, 
                                amount_paid=transaction.amount_paid,
                                pending_amount=pending_amount,
                                description=transaction.description)    
        df.append(new_row_df)
        isFirstTransaction=False

    if pending_amount>0:
        new_row_df=create_transaction_entry(
                                id=None,
                                bill_id=bill.id,
                                bill_number=bill.bill_number,
                                roi=roi,
                                bank_transaction_id=None,
                                payment_mode=None,
                                bill_date=bill.bill_date,
                                due_date=bill.due_date,
                                payment_date=datetime.now(),
                                bill_amount=bill.amount if pending_amount== bill.amount else None,
                                amount_paid=0.0,
                                pending_amount=pending_amount,
                                description="No payment made yet")    
        df.append(new_row_df)

    return df
             

def create_transaction_entry(
        id:int,
        bill_id:int,bill_number:int,roi:float, bank_transaction_id:str|None,payment_mode:str|None,    bill_date:datetime|None,due_date:datetime, payment_date:datetime|None, bill_amount:float|None,  amount_paid:float,pending_amount:float,description:str):
    delayed_days = (payment_date - due_date).days 
    if delayed_days < 0:
            delayed_days = 0
    penalty=amount_paid*(roi/100)*(delayed_days/30)
    if amount_paid==0 and delayed_days>0:
        penalty=pending_amount*(roi/100)*(delayed_days/30)
        
    data = {
            "id": id,    
            "bill_id": bill_id,
            "bill_number": bill_number,
            "bank_transaction_id": bank_transaction_id,
            "payment_mode":payment_mode,
            "bill_date":bill_date,
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

@router.get("/{company_id}/bills")
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

@router.get("/{company_id}/transactions")
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

@router.get("/download_to_excel/{company_id}")
def download_company_transaction_excel(request: Request,company_id:int, db=Depends(get_db)):
    company =company_api.get_company(id=company_id, db=db)
    transactions_df=create_transactions_for_company(company=company,roi=2)
   
    total_penalty=sum([tx["penalty"] for tx in transactions_df])
    total_pending=sum([tx["pending_amount"] for tx in transactions_df])
    
    df = pd.DataFrame(transactions_df)
    df_summary = pd.DataFrame([{
        "Total Penalty": total_penalty,
        "Total Pending Amount": total_pending,
        "Total Amount": total_penalty + total_pending
    }])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Transactions')
        df_summary.to_excel(writer, index=False, sheet_name='Summary')
        writer.close()
    output.seek(0)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{company.name}_transactions.xlsx"'
    }
    
    return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)