from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository import transaction as transaction_repo
from schemas.transaction import CreateTransaction,ShowTransaction

router = APIRouter()
@router.post("",status_code=status.HTTP_201_CREATED,response_model=ShowTransaction)
def create_transaction(transaction_create:transaction_repo.CreateTransaction,db:Session=Depends(get_db)):
    new_transaction=transaction_repo.create_transaction(transaction= transaction_create,db=db)
    return new_transaction

@router.get("/{id}",response_model=ShowTransaction)
def get_transaction_by_id(id:int,db:Session=Depends(get_db)):
    transaction=transaction_repo.get_transaction_with_404_exception(transaction_id=id,db=db)
    return transaction

@router.delete("/{id}")
def delete_transaction(id:int,db:Session=Depends(get_db)):
    _=transaction_repo.get_transaction_with_404_exception(transaction_id=id,db=db)
    result=transaction_repo.delete_transaction(transaction_id=id,db=db)
    return result

@router.get("/by-bill/{bill_id}",response_model=list[ShowTransaction])
def list_transactions_by_bill_id(bill_id:int,db:Session=Depends(get_db)):
    transactions=transaction_repo.get_all_transactions_by_bill_id(bill_id=bill_id,db=db)
    return transactions

@router.patch("",response_model=ShowTransaction)
def update_transaction(transaction_update:transaction_repo.UpdateTransaction,db:Session=Depends(get_db)):
    _ = transaction_repo.get_transaction_with_404_exception(transaction_id=transaction_update.id,db=db)
    updated_transaction=transaction_repo.update_transaction(transaction_update=transaction_update,db=db)
    return updated_transaction