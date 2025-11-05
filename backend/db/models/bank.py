# from db.base_class import Base 
# from sqlalchemy import Boolean, Column, Integer, String,Float,ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime,timedelta

# class Bank(Base):
#     __tablename__ = "banks"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=False, index=False, nullable=False)
#     branch = Column(String, nullable=True)
#     ifsc_code = Column(String, unique=True, index=True, nullable=False)
#     account_number = Column(String, unique=True, index=True, nullable=False)
#     transactions = relationship("Transaction", back_populates="bank")