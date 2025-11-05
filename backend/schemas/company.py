
from typing import Annotated
from pydantic import AfterValidator, BaseModel, ConfigDict, model_validator
from datetime import datetime

from core.utils.validator import PositiveIntStringOrNone

class CompanyCreate(BaseModel):
    name: str
    gst_number: str
    email: str | None = None
    phone_number: PositiveIntStringOrNone
    payment_term_days:int = 30
    address : str | None = None


    



class CompanyUpdate(BaseModel):
    id : int
    name: str | None = None
    gst_number: str | None = None
    email: str | None = None
    phone_number: PositiveIntStringOrNone
    payment_term_days:int | None = None
    address : str | None = None

class CompanyShow(CompanyCreate):
    id : int    
    model_config = ConfigDict(from_attributes=True)
    
class CompanyBrief(BaseModel):
    id: int
    payment_term_days: int
    model_config = ConfigDict(from_attributes=True)

