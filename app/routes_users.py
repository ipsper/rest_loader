from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .models import User
from .dbase_api import get_db

# Pydantic model for the request body
class UserCreate(BaseModel):
    name: str
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
        new_user = User(name=user.name, email=user.email, street=user.street, street_number=user.street_number, city=user.city, zip=user.zip, country=user.country)
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