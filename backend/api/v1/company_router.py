
from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.company import create_company,get_company_by_id,update_company,delete_company,get_company_by_gst_number,get_all_company
from schemas.company import CompanyCreate,CompanyUpdate,CompanyShow
router = APIRouter()
@router.post("",response_model=CompanyShow,status_code=status.HTTP_201_CREATED)
def create_new_company(company:CompanyCreate,db:Session=Depends(get_db)):
    db_company = get_company_by_gst_number(gst_number=company.gst_number,db=db)
    if db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Company with this GST number already exists")
    new_company = create_company(company=company,db=db)
    return new_company

@router.get("/{id}",response_model=CompanyShow,status_code=status.HTTP_200_OK)
def get_company(id:int,db:Session=Depends(get_db)):
    db_company = get_company_by_id(company_id=id,db=db)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Company not found")
    return db_company

@router.patch("",response_model=CompanyShow,status_code=status.HTTP_200_OK)
def update_existing_company(company:CompanyUpdate,db:Session=Depends(get_db)):
    db_company = get_company_by_id(company_id=company.id,db=db)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Company not found")
    updated_company = update_company(company_update=company,db=db)
    return updated_company

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_existing_company(id:int,db:Session=Depends(get_db)):
    company= get_company_by_id(company_id=id,db=db)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Company not found")
       
    result = delete_company(company_id=id,db=db)
    return result

@router.get("",status_code=status.HTTP_200_OK,response_model=list[CompanyShow])
def get_all_companies(db:Session=Depends(get_db)):
    companies = get_all_company(db=db)
    return companies