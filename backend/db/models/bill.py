from db.base_class import Base 
from sqlalchemy import Boolean, Column, Integer, String,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import timedelta,datetime

class Bill(Base):
    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(Integer,unique=True,nullable=False)
    amount = Column(Float, nullable=False)
    bill_date = Column(DateTime, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="bills")
    transactions = relationship("Transaction", back_populates="bill", cascade="all, delete-orphan")
    @property
    def due_date(self):
        if self.bill_date and self.company:
            return self.bill_date + timedelta(days=self.company.payment_term_days)
        return None


    