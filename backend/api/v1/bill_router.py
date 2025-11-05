from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository import bill as billrepo 
from schemas.bill import BillCreate,BillUpdate,BillShow


router = APIRouter()
@router.post("",status_code=status.HTTP_201_CREATED,response_model=BillShow)
def create_bill(bill_create:BillCreate,db:Session=Depends(get_db)):
    new_bill=billrepo.create_new_bill(bill= bill_create,db=db)
    return new_bill


@router.get("/{id}",response_model=BillShow)
def get_bill_by_id(id:int,db:Session=Depends(get_db)):
    bill=billrepo.get_bill_with_not_found_exception(id=id,db=db)
    return bill

@router.patch("",response_model=BillShow)
def update_bill(bill_update:BillUpdate,db:Session=Depends(get_db)):
    _=billrepo.get_bill_with_not_found_exception(id=bill_update.id,db=db)    
  
    updated_bill=billrepo.update_bill(bill_update=bill_update,db=db)
    return updated_bill

@router.delete("/{id}")
def delete_bill(id:int,db:Session=Depends(get_db)):
    _=billrepo.get_bill_with_not_found_exception(id=id,db=db) 
    result=billrepo.delete_bill(id=id,db=db)
    return result

@router.get("/by-company/{id}",response_model=list[BillShow])
def list_bills_by_company_id(id:int,db:Session=Depends(get_db)):
    bills=billrepo.get_all_bills_by_company_id(company_id=id,db=db)
    return bills