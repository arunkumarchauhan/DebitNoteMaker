from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from db.models.transaction import Transaction
from schemas.transaction import CreateTransaction,UpdateTransaction
from db.repository.bill import get_bill_by_bill_number

def create_transaction(transaction:CreateTransaction,db:Session):
    json = transaction.model_dump()
    print(json)
    if 'bill_number' in json:
        del json["bill_number"]
    new_transaction = Transaction(**json)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_transaction(transaction_id:int,db:Session):
   transaction= db.query(Transaction).filter(Transaction.id == transaction_id).first()
   return transaction

def update_transaction(transaction_update:UpdateTransaction,db:Session):
    if transaction_update.bill_number and transaction_update.bill_id is None:
        bill= get_bill_by_bill_number(bill_number=transaction_update.bill_number,db=db)
        if  bill:
            transaction_update.bill_id= bill.id
            transaction_update.bill_id= bill.id

    transaction= get_transaction(transaction_id=transaction_update.id,db=db)
    update_data = transaction_update.model_dump(exclude_unset=True)
   
    for key, value in update_data.items():
        setattr(transaction, key, value)
    db.add(transaction)
    db.commit()
    return transaction

def delete_transaction(transaction_id:int,db:Session):
    transaction= get_transaction(transaction_id=transaction_id,db=db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"msg": f"Transaction with id {transaction.id} deleted successfully"}

def get_all_transactions_by_bill_id(bill_id:int,db:Session):
    transactions= db.query(Transaction).filter(Transaction.bill_id == bill_id).all()
    return transactions

def get_transaction_with_404_exception(transaction_id:int,db:Session):
    transaction = get_transaction(transaction_id=transaction_id,db=db)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Transaction not found")
    return transaction