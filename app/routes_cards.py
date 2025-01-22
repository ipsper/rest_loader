from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .dbase_api import SessionLocal
from .models import Card
from .dbase_api import get_db

# Pydantic model for the request body
class CardCreate(BaseModel):
    cardnumber: str
    month_year: str
    cvc: str
    cardholder: str

# Create a router for the cards endpoints
router = APIRouter()

# Endpoint to create a new card
@router.post("/cards/")
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    try:
        new_card = Card(cardnumber=card.cardnumber, month_year=card.month_year, 
                        cvc=card.cvc, cardholder=card.cardholder)
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        logger.info("Card added successfully", extra={"card": new_card})
        return {"message": "Card added successfully", "card": new_card}
    except Exception as e:
        db.rollback()
        logger.error("Error adding card", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Endpoint to read all cards from the database
@router.get("/cards/")
def read_cards(db: Session = Depends(get_db)):
    try:
        cards = db.query(Card).all()
        logger.info("Fetched all cards")
        return {"cards": cards}
    except Exception as e:
        logger.error("Error fetching cards", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Ta bort en användare baserat på ID
@router.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    try:
        card = db.query(Card).filter(Card.id == card_id).first()
        if card is None:
            raise HTTPException(status_code=404, detail="Card not found")
        db.delete(card)
        db.commit()
        logger.info("Card deleted successfully", extra={"card_id": card_id})
        return {"message": "Card deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting card", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")