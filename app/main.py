from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .routes_cards import router as cards_router  # Import the cards router
from .routes_tables import router as tables_router  # Import the cards router
from .routes_users import router as users_router  # Import the cards router
from .routes_store import router as users_store # Import the cards router
from .routes_purchase import router as users_purchase  # Import the cards router
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

# Include the cards router
app.include_router(cards_router)
app.include_router(tables_router)
app.include_router(users_router)
app.include_router(users_store)
app.include_router(users_purchase)
