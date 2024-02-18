from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
import chardet
from io import StringIO
import pandas as pd
import shutil
import os
import schemas
from sqlalchemy.orm import Session
from app.Models import models
from database import clear_database
from typing import List

router = APIRouter()

@router.post("/display-table")
async def display_table(file: UploadFile = Form(...), db: Session = Depends(models.get_db)):
    clear_database()
    directory = "./data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    with open(f"data/{file.filename}", 'rb') as f:
        result = chardet.detect(f.read())  # or readline if the file is large
    
    
        
    # ------------------------------- Create Company ------------------------------
    review = pd.read_excel(f"data/{file.filename}", sheet_name="Main table")
    review = review.replace([pd.NaT, pd.NA, float('nan'), float('inf'), float('-inf')], None)
    data_dict = {col: review[col].tolist() for col in review.columns}
    
    list_company_name = data_dict["Company Name"]
    list_IPO_Year = data_dict["IPO Year"]
    list_primary_business  = data_dict["Primary Business "]
    list_pre_IPO = data_dict["Pre-IPO money raised ($, millions)"]
    length = min(len(list_company_name), len(list_IPO_Year), len(list_primary_business), len(list_pre_IPO))
    print(length)
    for i in range(0, length):
        main_dict = {
            "company_name": list_company_name[i],
            "IPO_year": list_IPO_Year[i],
            "primary_business": list_primary_business[i],
            "pre_IPO": str(list_pre_IPO[i])
        }
        print(type(main_dict["pre_IPO"]))
        if list_company_name[i] == None:
            continue
        db_main = models.get_main_by_name(db, list_company_name[i])
        # print(db_main.company_name, " - ", list_company_name[i])
        if not db_main:
            # print(db_main.company_name)
            print(models.create_main(db, schemas.MainCreate(**main_dict)))
    
    # ------------------------------- Create Human ------------------------------
    
    review = pd.read_excel(f"data/{file.filename}", sheet_name="Human")
    review = review.replace([pd.NaT, pd.NA, float('nan'), float('inf'), float('-inf')], None)
    data_dict = {col: review[col].tolist() for col in review.columns}
    
    list_name = data_dict["Name of a person"]
    list_founder = data_dict["Founder (yes/no)"]
    list_founder_role  = data_dict["Founder role at Company"]
    list_company_name = data_dict["Company name"]
    list_founder_organization = data_dict["Founder org"]
    list_type_of_org = data_dict["Type of org"]
    list_equity = data_dict["Founder equity at IPO (%)"]
    length = min(len(list_name), len(list_founder), len(list_founder_role), len(list_company_name), len(list_founder_organization), len(list_type_of_org), len(list_equity))
    print(length)
    for i in range(0, length):
        if list_company_name[i] == None:
            continue
        db_main = models.get_main_by_name(db, list_company_name[i])
        if db_main:
            human_dict = {
                "name": list_name[i],
                "founder": list_founder[i],
                "founder_role": list_founder_role[i],
                "company_name": list_company_name[i],
                "founder_organization": list_founder_organization[i],
                "type_of_org": list_type_of_org[i],
                "equity": str(list_equity[i]),
                "owner_id": db_main.id
            }
            models.create_human(db, schemas.HumanCreate(**human_dict))
            
    # --------------------- create_intellectualProperty ------------------------
    
    review = pd.read_excel(f"data/{file.filename}", sheet_name="Intellectual Property")
    review = review.replace([pd.NaT, pd.NA, float('nan'), float('inf'), float('-inf')], None)
    data_dict = {col: review[col].tolist() for col in review.columns}
    
    list_licensor_organization = data_dict["Licensor (seller) organization"]
    list_type_of_agreement = data_dict["Type of Agreement"]
    list_licensee_organization  = data_dict["Organization"]
    list_academic_licensor = data_dict["Academic Licensor (Yes/ No)"]
    length = min(len(list_licensor_organization), len(list_type_of_agreement), len(list_licensee_organization), len(list_academic_licensor))
    
    for i in range(0, length):
        if list_licensee_organization[i] == None:
            continue
        db_main = models.get_main_by_name(db, list_licensee_organization[i])
        if db_main:
            # print(db_main.id, " ", db_main.company_name, " ", list_licensee_organization[i])
            intellectualProperty_dict = {
                "licensor_organization": list_licensor_organization[i],
                "type_of_agreement": list_type_of_agreement[i],
                "licensee_organization": list_licensee_organization[i],
                "academic_licensor": list_academic_licensor[i],
                "owner_id": db_main.id
            }
            # print(intellectualProperty_dict)
            models.create_intellectualProperty(db, schemas.IntellectualPropertyCreate(**intellectualProperty_dict))
    return True

# ----------------------- Main Table ----------------------------


@router.post("/company", response_model=schemas.Main)
def create_main(main: schemas.MainCreate, db: Session = Depends(models.get_db)):
    print(main.company_name)
    db_main = models.get_main_by_name(db, main.company_name)
    if db_main:
        raise HTTPException(status_code=400, detail="Name already registered")
    return models.create_main(db, main)

@router.get("/company", response_model=List[schemas.Main])
def read_mains(db: Session = Depends(models.get_db)):
    mains = models.get_mains(db)
    sorted_mains = sorted(mains, key=lambda x: x.id)
    return sorted_mains

@router.put("/company/{id}", response_model=schemas.Main)
def update_main(id: int, main: schemas.MainCreate, db: Session = Depends(models.get_db)):
    print(main)
    db_main = models.get_main_by_id(db, id)
    if db_main is None:
        raise HTTPException(status_code=404, detail="Main not found")
    return models.update_main(db, db_main, main)

@router.delete("/company/{id}")
def delete_main(id: int, db: Session = Depends(models.get_db)):
    db_main = models.get_main_by_id(db, id)
    # print(db_main.humans, " ", db_main.company_name)
    # return schemas.Main(db_main)
    if db_main is None:
        raise HTTPException(status_code=404, detail="Main not found")
    print(models.delete_main(db, db_main))
    return True

# ----------------------- Human Table ----------------------------

@router.post("/human", response_model=schemas.Human)
def create_human(human: schemas.HumanCreate, db: Session = Depends(models.get_db)):
    print(human.name)
    db_main = models.get_main_by_id(db, human.owner_id)
    if not db_main:
        raise HTTPException(status_code=404, detail="Main not found")
    return models.create_human(db, human)

@router.get("/human", response_model=List[schemas.Human])
def read_humans(db: Session = Depends(models.get_db)):
    humans = models.get_humans(db)
    sorted_humans = sorted(humans, key=lambda x: x.id)
    return sorted_humans

@router.put("/human/{id}", response_model=schemas.Human)
def update_human(id: int, human: schemas.HumanCreate, db: Session = Depends(models.get_db)):
    print(human)
    db_human = models.get_human_by_id(db, id)
    if db_human is None:
        raise HTTPException(status_code=404, detail="Human not found")
    return models.update_human(db, db_human, human)

@router.delete("/human/{id}")
def delete_human(id: int, db: Session = Depends(models.get_db)):
    db_human = models.get_human_by_id(db, id)
    if db_human is None:
        raise HTTPException(status_code=404, detail="Main not found")
    print(models.delete_human(db, db_human))
    return True


# ----------------------- Intellectual Property Table ----------------------------

@router.post("/intellectualProperty", response_model=schemas.IntellectualProperty)
def create_intellectualProperty(intellectualProperty: schemas.IntellectualPropertyCreate, db: Session = Depends(models.get_db)):
    print(intellectualProperty)
    db_main = models.get_main_by_id(db, intellectualProperty.owner_id)
    print(db_main)
    if not db_main:
        raise HTTPException(status_code=404, detail="Main not found")
    return models.create_intellectualProperty(db, intellectualProperty)

@router.get("/intellectualProperty", response_model=List[schemas.IntellectualProperty])
def read_intellectualProperty(db: Session = Depends(models.get_db)):
    intellectualProperties = models.get_intellectualProperty(db)
    sorted_intellectualProperties = sorted(intellectualProperties, key=lambda x: x.id)
    return sorted_intellectualProperties

@router.put("/intellectualProperty/{id}", response_model=schemas.IntellectualProperty)
def update_intellectualProperty(id: int, intellectualProperty: schemas.IntellectualPropertyCreate, db: Session = Depends(models.get_db)):
    print(intellectualProperty)
    db_intellectualProperty = models.get_intellectualProperty_by_id(db, id)
    if db_intellectualProperty is None:
        raise HTTPException(status_code=404, detail="IntellectualProperty not found")
    return models.update_intellectualProperty(db, db_intellectualProperty, intellectualProperty)

@router.delete("/intellectualProperty/{id}")
def delete_intellectualProperty(id: int, db: Session = Depends(models.get_db)):
    db_intellectualProperty = models.get_intellectualProperty_by_id(db, id)
    if db_intellectualProperty is None:
        raise HTTPException(status_code=404, detail="Main not found")
    print(models.delete_intellectualProperty(db, db_intellectualProperty))
    return True