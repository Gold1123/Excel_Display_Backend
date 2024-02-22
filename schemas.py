from pydantic import BaseModel
from typing import List

from pydantic import BaseModel
from typing import List, Optional

class HumanBase(BaseModel):
    name: Optional[str] = None
    founder: Optional[str] = None
    founder_role: Optional[str] = None
    company_name: Optional[str] = None
    founder_organization: Optional[str] = None
    type_of_org: Optional[str] = None
    equity: Optional[str] = None
    
    
class HumanCreate(HumanBase):
    owner_id: Optional[int]

class Human(HumanCreate):
    id: int

    class Config:
        orm_mode = True

class IntellectualPropertyBase(BaseModel):
    licensor_organization: Optional[str] = None
    type_of_licensor_organization: Optional[str] = None
    type_of_agreement: Optional[str] = None
    licensee_organization: Optional[str] = None
    academic_licensor: Optional[str] = None
    Equity_in_the_License_Agreement: Optional[str] = None
    Direct_equity_to_inventor_academia: Optional[str] = None
    Direct_equity_to_Inventor_operator: Optional[str] = None
    Direcct_academic_institution_equity: Optional[str] = None
    
    

class IntellectualPropertyCreate(IntellectualPropertyBase):
    owner_id: Optional[int]

class IntellectualProperty(IntellectualPropertyCreate):
    id: int

    class Config:
        orm_mode = True

class MainBase(BaseModel):
    company_name: Optional[str] = None
    IPO_year: Optional[int] = None
    primary_business: Optional[str] = None
    pre_IPO: Optional[str] = None
    
    
class MainCreate(MainBase):
    pass

class Main(MainBase):
    id: int
    humans: List[Human] = []
    intellectual_properties: List[IntellectualProperty] = []

    class Config:
        orm_mode = True
        from_attributes=True