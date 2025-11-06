from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from db.models.bill import Bill
from schemas.bill import BillCreate,BillUpdate,BillShow
from sqlalchemy.orm import selectinload

def create_new_bill(bill:BillCreate,db:Session):
    existing_bill=get_bill_by_bill_number(bill_number=bill.bill_number,db=db)
    if existing_bill:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bill with this bill number already exists")
    new_bill = Bill(**bill.model_dump(exclude_none=True))
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill

def get_bill(id:int,db:Session):
   bill= db.query(Bill).options(selectinload(Bill.company)).filter(Bill.id == id).first()
   return bill

def get_bill_by_bill_number(bill_number:str,db:Session):
    bill= db.query(Bill).filter(Bill.bill_number == bill_number).first()
    return bill
def update_bill(bill_update:BillUpdate,db:Session):
    bill= get_bill(id=bill_update.id,db=db)
    update_data = bill_update.model_dump(exclude_unset=True)
   
    for key, value in update_data.items():
        setattr(bill, key, value)
    db.add(bill)
    db.commit()
    return bill
def delete_bill(id:int,db:Session):
    bill= get_bill(id=id,db=db)

    db.delete(bill)
    db.commit()
    return {"msg": f"Bill with id {bill.id} deleted successfully"}

def get_all_bills_by_company_id(company_id:int,db:Session):
    bills = db.query(Bill).filter(Bill.company_id == company_id).all()
    return bills

def get_bill_with_not_found_exception(id:int,db:Session):
    bill= get_bill(id=id,db=db)
    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bill not found")
    return bill

