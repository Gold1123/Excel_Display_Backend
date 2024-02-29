from fastapi import Depends
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.orm import Session
import schemas
from typing import List
from database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder

limit = 500

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Main(Base): 
    __tablename__ = "mains"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    IPO_year = Column(Integer, index=True)
    primary_business = Column(String)
    pre_IPO = Column(String)
    non_founder_ceo_equity = Column(Float)
    total_founder_equity = Column(Float)
    
    humans = relationship("Human", back_populates="owner")
    intellectual_properties = relationship("Intellectual_property", back_populates="owner")
    
class Human(Base):
    __tablename__ = "humans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    founder = Column(String, index=True)
    founder_role = Column(String)
    company_name = Column(String)
    founder_organization = Column(String)
    type_of_org = Column(String)
    equity = Column(Float)
    
    owner_id = Column(Integer, ForeignKey("mains.id"))
    
    owner = relationship("Main", back_populates="humans")

class Intellectual_property(Base):
    __tablename__ = "intellectual_properties"
    
    id = Column(Integer, primary_key=True, index=True)
    licensor_organization = Column(String, index=True)
    type_of_licensor_organization = Column(String, index = True)
    type_of_agreement = Column(String, index=True)
    licensee_organization = Column(String, index=True)
    academic_licensor = Column(String, index=True)
    equity_in_the_License_Agreement = Column(String, index = True)
    direct_equity_to_inventor_academia = Column(Float, index = True)
    direct_equity_to_Inventor_operator = Column(Float, index = True)
    direct_academic_institution_equity = Column(Float, index = True)
    contract_doc = Column(String, index=True)
    
    owner_id = Column(Integer, ForeignKey("mains.id"))
    
    owner = relationship("Main", back_populates="intellectual_properties")
    


# ----------------------- Main Table ----------------------------

def get_main_by_name(db: Session, name: str):
    return db.query(Main).filter(Main.company_name == name).first()

def get_main_by_id(db: Session, id: int):
    return db.query(Main).filter(Main.id == id).first()

def get_mains(db: Session, skip: int = 0, limit: int = limit):
    return db.query(Main).offset(skip).limit(limit).all()
    
def create_main(db: Session, main: schemas.MainCreate):
    db_main = Main(**main.dict())
    db.add(db_main)
    db.commit()
    db.refresh(db_main)
    return db_main

def update_main(db: Session, db_main: Main, main_in: schemas.MainCreate):
    main_data = jsonable_encoder(db_main)
    update_data = main_in.dict(exclude_unset=True)
    for field in main_data:
        if field in update_data:
            setattr(db_main, field, update_data[field])
    db.add(db_main)
    db.commit()
    db.refresh(db_main)
    return db_main

def delete_main(db: Session, db_main: Main):
    db.delete(db_main)
    db.commit()
    return db_main

# ----------------------- Human Table ----------------------------

def create_human(db: Session, human: schemas.HumanCreate):
    print(human.dict())
    db_human = Human(**human.dict())
    db.add(db_human)
    db.commit()
    db.refresh(db_human)
    return db_human

def get_humans(db: Session, skip: int = 0, limit: int = limit):
    return db.query(Human).offset(skip).limit(limit).all()

def update_human(db: Session, db_human: Main, human_in: schemas.MainCreate):
    human_data = jsonable_encoder(db_human)
    update_data = human_in.dict(exclude_unset=True)
    for field in human_data:
        if field in update_data:
            setattr(db_human, field, update_data[field])
    db.add(db_human)
    db.commit()
    db.refresh(db_human)
    return db_human


def get_human_by_id(db: Session, id: int):
    return db.query(Human).filter(Human.id == id).first()

def delete_human(db: Session, db_human: Human):
    db.delete(db_human)
    db.commit()
    return db_human



# ----------------------- Intellectual Property Table ----------------------------

def create_intellectualProperty(db: Session, intellectualProperty: schemas.IntellectualPropertyCreate):
    db_intellectualProperty = Intellectual_property(**intellectualProperty.dict())
    db.add(db_intellectualProperty)
    db.commit()
    db.refresh(db_intellectualProperty)
    return db_intellectualProperty

def get_intellectualProperty(db: Session, skip: int = 0, limit: int = limit):
    return db.query(Intellectual_property).offset(skip).limit(limit).all()

def get_intellectualProperty_by_id(db: Session, id: int):
    print(id)
    return db.query(Intellectual_property).filter(Intellectual_property.id == id).first()

def update_intellectualProperty(db: Session, db_intellectualProperty: Main, intellectualProperty_in: schemas.MainCreate):
    intellectualProperty_data = jsonable_encoder(db_intellectualProperty)
    update_data = intellectualProperty_in.dict(exclude_unset=True)
    for field in intellectualProperty_data:
        if field in update_data:
            setattr(db_intellectualProperty, field, update_data[field])
    db.add(db_intellectualProperty)
    db.commit()
    db.refresh(db_intellectualProperty)
    return db_intellectualProperty

def delete_intellectualProperty(db: Session, db_intellectualProperty: Human):
    db.delete(db_intellectualProperty)
    db.commit()
    return db_intellectualProperty