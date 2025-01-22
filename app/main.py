from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .routes_cards import router as cards_router  # Import the cards router
from .routes_tables import router as tables_router  # Import the cards router
from .dbase_api import SessionLocal, init_db
from .models import User

init_db()

app = FastAPI()

# Dependency för att få en databas-session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class UserCreate(BaseModel):
    name: str
    email: str

# Lägg till en ny användare
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = User(name=user.name, email=user.email)
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
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        logger.info("Fetched all users")
        return {"users": users}
    except Exception as e:
        logger.error("Error fetching users", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Ta bort en användare baserat på ID
@app.delete("/users/{user_id}")
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

# Include the cards router
app.include_router(cards_router)
app.include_router(tables_router)