from db.base_class import Base 
from sqlalchemy import Boolean, Column, Integer, String,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False, nullable=False)
    gst_number = Column(String, unique=True, index=True, nullable=False)
    email =  Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    payment_term_days = Column(Integer, nullable=False, default=30)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    bills = relationship("Bill", back_populates="company", cascade="all, delete-orphan")