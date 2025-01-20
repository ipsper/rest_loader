from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import logging

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Logger setup
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

class UserCreate(BaseModel):
    name: str
    email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        logger.info("Fetched all users")
        return {"users": users}
    except Exception as e:
        logger.error("Error fetching users", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Include the cards router
app.include_router(cards_router)