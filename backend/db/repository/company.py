from db.models.company import Company
from schemas.company import CompanyCreate, CompanyUpdate, CompanyShow
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
def create_company(company:CompanyCreate,db:Session,):
    new_company = Company(**company.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

def get_company_by_id(company_id:int,db:Session):
   company= db.query(Company).filter(Company.id == company_id).first()
   return company
def get_company_by_gst_number(gst_number:str,db:Session):
    company= db.query(Company).filter(Company.gst_number == gst_number).first()
    return company

def update_company(company_update:CompanyUpdate,db:Session):
    company= get_company_by_id(company_id=company_update.id,db=db)

    update_data = company_update.model_dump(exclude_unset=True)
   
    for key, value in update_data.items():
        setattr(company, key, value)
    db.add(company)
    db.commit()
    return company

def delete_company(company_id:int,db:Session):
    company= get_company_by_id(company_id=company_id,db=db)
    db.delete(company)
    db.commit()
    return {"msg": f"Company with id {company.id} and name {company.name} deleted successfully"}

def get_all_company(db:Session):
    companies = db.query(Company).all()
    return companies