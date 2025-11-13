

from pydantic import BaseModel, ConfigDict, computed_field, model_validator
from datetime import datetime,timezone,timedelta

from schemas.company import CompanyBrief

class BillCreate(BaseModel):
    bill_number : int
    amount : float
    bill_date:datetime
    company_id:int

class BillUpdate(BaseModel):
    id:int
    bill_number : int | None = None
    amount : float | None = None
    bill_date:datetime | None = None
    company_id:int | None = None    
    
class BillShow(BillCreate):
    id:int
    due_date: datetime | None = None
    # delayed_days: int | None = None
    model_config = ConfigDict(from_attributes=True)
    

    # @computed_field(return_type=datetime | None)
    # def due_date(self):
    #     """Compute due date dynamically based on company's payment terms."""
    #     if self.company:
    #         return self.bill_date + timedelta(days=self.company.payment_term_days)
    #     return None  
      
    # @computed_field(return_type=int | None)
    # def delayed_days(self) -> int | None:
    #     if not self.due_date:
    #         return None
    #     now = datetime.now()
    #     delta = (now - self.due_date).days
    #     return max(delta, 0)