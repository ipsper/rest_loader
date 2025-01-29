from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from faker import Faker
import json
from .logger_config import logger
from .models import Card
from .dbase_api import get_db

# Pydantic model for the request body
class CardCreate(BaseModel):
    cardnumber: str
    month_year: str
    cvc: str
    cardholder: str

class CardholderRequest(BaseModel):
    cardholder: str

# Create a router for the cards endpoints
router = APIRouter()
fake = Faker()

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
    
# Endpoint to get all card info by id
@router.get("/cards/{card_id}")
def get_card_by_id(card_id: int, db: Session = Depends(get_db)):
    try:
        card = db.query(Card).filter(Card.id == card_id).first()
        if card is None:
            raise HTTPException(status_code=404, detail="Card not found")
        logger.info("Fetched card info", extra={"card_id": card_id})
        return card
    except Exception as e:
        logger.error("Error fetching card info", exc_info=True)
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
    
# Endpoint to count all cards in the database
@router.get("/cards/count/")
def count_cards(db: Session = Depends(get_db)):
    try:
        count = db.query(Card).count()
        logger.info("Counted all cards", extra={"count": count})
        return {"count": count}
    except Exception as e:
        logger.error("Error counting cards", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

# Endpoint to count unique cardholders in the database
@router.get("/cards/cardholders/count/")
def count_unique_cardholders(db: Session = Depends(get_db)):
    try:
        count = db.query(func.count(func.distinct(Card.cardholder))).scalar()
        logger.info("Counted unique cardholders", extra={"count": count})
        return {"count": count}
    except Exception as e:
        logger.error("Error counting unique cardholders", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Function to count all occurrences of the same cardholder
def count_cardholder_occurrences(cardholder: str, db: Session):
    try:
        count = db.query(func.count(Card.id)).filter(Card.cardholder == cardholder).scalar()
        logger.info(f"Counted occurrences of cardholder {cardholder}", extra={"count": count})
        return count
    except Exception as e:
        logger.error(f"Error counting occurrences of cardholder {cardholder}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to count all occurrences of a specific cardholder
@router.post("/cards/cardholder/count/")
def count_cardholder(request: CardholderRequest, db: Session = Depends(get_db)):
    count = count_cardholder_occurrences(request.cardholder, db)
    return {"cardholder": request.cardholder, "count": count}

# Endpoint to list all cardholders and their ids
@router.get("/cards/cardholders/")
def list_cardholders(db: Session = Depends(get_db)):
    try:
        cardholders = db.query(Card.id, Card.cardholder).all()
        logger.info("Fetched all cardholders and their ids")
        return {"cardholders": [{"id": card.id, "cardholder": card.cardholder} for card in cardholders]}
    except Exception as e:
        logger.error("Error fetching cardholders", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/generate_credit_cards")
def generate_credit_cards(count: int = Query(default=1, ge=1)):
    try:
        credit_cards = []
        for _ in range(count):
            credit_card = {
                "card_number": fake.credit_card_number(),
                "expiry_date": fake.credit_card_expire(),
                "name": fake.name(),
                "cvc": fake.credit_card_security_code()
            }
            credit_cards.append(credit_card)
        return {"credit_cards": credit_cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")