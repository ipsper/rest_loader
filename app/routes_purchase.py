from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .models import Purch
from .dbase_api import get_db

# Pydantic model for the request body
class DoPurchase(BaseModel):
    productid: str
    totality: str
    number: str

# Create a router for the cards endpoints
router = APIRouter()

# gör ett köp
@router.post("/purchase/")
def do_purchase(purch: DoPurchase, db: Session = Depends(get_db)):
    try:
        new_purch = Purch(productid=purch.productid, prize=purch.prize, number=purch.number)
        db.add(new_purch)
        db.commit()
        db.refresh(new_purch)
        logger.info("Purchase added successfully", extra={"user": new_purch})
        return {"message": "Purchase added successfully", "user": new_purch}
    except Exception as e:
        db.rollback()
        logger.error("Error added a purchase", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Läs alla köp från databasen
@router.get("/purchase/")
def read_purchase(db: Session = Depends(get_db)):
    try:
        purchase = db.query(Purch).all()
        logger.info("Fetched all purchase")
        return {"purchase": purchase}
    except Exception as e:
        logger.error("Error fetching purchase", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Ta bort ett köp baserat på ID
@router.delete("/purchase/{id}")
def delete_purch(id: int, db: Session = Depends(get_db)):
    try:
        purch = db.query(Purch).filter(Purch.id == id).first()
        if purch is None:
            raise HTTPException(status_code=404, detail="Purch not found")
        db.delete(purch)
        db.commit()
        logger.info("Purchase deleted successfully", extra={"purchase id": id})
        return {"message": "purchase deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting purchase", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")