from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import json
import os
from collections import Counter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .models import User
from .dbase_api import get_db

# Pydantic model for the request body
class UserCreate(BaseModel):
    surname: str
    givenname: str
    email: str
    street: str
    street_number: str
    city: str
    zip: str
    country: str

# Create a router for the cards endpoints
router = APIRouter()

# Lägg till en ny användare
@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = User(surname=user.surname, givenname=user.givenname,  email=user.email, street=user.street, street_number=user.street_number, city=user.city, zip=user.zip, country=user.country)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info("User added successfully", extra={"user": new_user})
        return {"message": "User added successfully", "user": new_user}
    except Exception as e:
        db.rollback()
        logger.error("Error adding user", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Läs alla användare från databasen
@router.get("/users/")
def read_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        logger.info("Fetched all users")
        return {"users": users}
    except Exception as e:
        logger.error("Error fetching users", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Ta bort en användare baserat på ID
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        logger.info("User deleted successfully", extra={"user_id": user_id})
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting user", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Befintlig kod för build_names_json
def build_names_json(count):
    # Läs in swedish-male-names.json
    with open('swedish-male-names.json', 'r') as male_names_file:
        male_names = json.load(male_names_file)
    
    # Läs in surnames.json
    with open('surnames.json', 'r') as surnames_file:
        surnames = json.load(surnames_file)
    
    # Begränsa antalet namn till det minsta av count, längden på male_names och längden på surnames
    count = min(count, len(male_names), len(surnames))
    
    # Bygg JSON-strukturen
    names_json = []
    for i in range(count):
        firstname = male_names[i]
        surname = surnames[i]
        totalname = f"{firstname} {surname}"
        names_json.append({
            "index": i,
            "firstname": firstname,
            "surname": surname,
            "totalname": totalname
        })
    
    return names_json

# Ny funktion för att hitta dubbletter i en JSON-fil
def find_duplicates_in_json(items):
    # Använd Counter för att räkna förekomster av varje namn
    item_counts = Counter(items)
    # Filtrera ut namn som förekommer mer än en gång
    duplicates = [item for item, count in item_counts.items() if count > 1]
    return duplicates

# Ny endpoint för att hitta dubbletter i en JSON-fil
@router.post("/duplicates")
async def get_duplicates(file: UploadFile = File(...)):
    try:
        # Kontrollera om filen finns
        if not os.path.exists(file.filename):
            raise HTTPException(status_code=404, detail="File not found")

        content = await file.read()
        items = json.loads(content)
        duplicates = find_duplicates_in_json(items)
        return {"duplicates": duplicates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

