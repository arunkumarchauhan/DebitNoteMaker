from datetime import datetime
from sqlalchemy import  Column, Integer,  Text, DateTime, ForeignKey,Float,String
from sqlalchemy.orm import relationship
from db.base_class import Base 

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    bank_transaction_id = Column(String,nullable=True)
    payment_mode = Column(String, nullable=False)
    amount_paid = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    payment_date = Column(DateTime, default=datetime.now)
    bill_id = Column(Integer, ForeignKey("bill.id"))
    bill = relationship("Bill", back_populates="transactions")

    
