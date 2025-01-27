from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .models import Store
from .dbase_api import get_db

# Pydantic model for the request body
class Inventory(BaseModel):
    prodname: str
    productid: int
    instock: int
    prize: float

# Create a router for the cards endpoints
router = APIRouter()

# Lägg till en ny produkt 
@router.post("/stock/")
def add_produkt(stock: Inventory, db: Session = Depends(get_db)):
    try:
        new_produkt = Store(prodname=stock.prodname, productid=stock.productid, instock=stock.instock, prize=stock.prize)
        db.add(new_produkt)
        db.commit()
        db.refresh(new_produkt)
        logger.info("User added successfully", extra={"produkt": new_produkt})
        return {"message": "User added successfully", "produkt": new_produkt}
    except Exception as e:
        db.rollback()
        logger.error("Error adding produkt", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Läs alla produkter från databasen
@router.get("/stock/")
def read_stock(db: Session = Depends(get_db)):
    try:
        stock = db.query(Store).all()
        logger.info("Fetched all in stock")
        return {"stock": stock}
    except Exception as e:
        logger.error("Error fetching stock", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Ta bort en produkt baserat på ID från lagret
@router.delete("/stock/{productid}")
def delete_produkt(productid: int, db: Session = Depends(get_db)):
    try:
        produkt = db.query(Store).filter(Store.productid == productid).first()
        if produkt is None:
            raise HTTPException(status_code=404, detail="Produkt not found")
        db.delete(produkt)
        db.commit()
        logger.info("Produkt deleted successfully", extra={"prod_id": prod_id})
        return {"message": "Produkt deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting produkt", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Endpoint to decrease the stock of a product
@router.post("/stock/decrease/")
def decrease_stock(productid: int, amount: int, db: Session = Depends(get_db)):
    try:
        produkt = db.query(Store).filter(Store.productid == productid).first()
        if produkt is None:
            raise HTTPException(status_code=404, detail="Produkt not found")
        if produkt.instock < amount:
            raise HTTPException(status_code=400, detail="Not enough stock")
        produkt.instock -= amount
        db.commit()
        logger.info("Decreased stock successfully", extra={"productid": productid, "amount": amount})
        return {"message": "Decreased stock successfully", "productid": productid, "new_stock": produkt.instock}
    except Exception as e:
        db.rollback()
        logger.error("Error decreasing stock", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Function to increase the stock of a product
def increase_stock(productid: int, amount: int, db: Session):
    try:
        produkt = db.query(Store).filter(Store.productid == productid).first()
        if produkt is None:
            raise HTTPException(status_code=404, detail="Produkt not found")
        produkt.instock += amount
        db.commit()
        logger.info("Increased stock successfully", extra={"productid": productid, "amount": amount})
        return {"message": "Increased stock successfully", "productid": productid, "new_stock": produkt.instock}
    except Exception as e:
        db.rollback()
        logger.error("Error increasing stock", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to increase the stock of a product
@router.post("/stock/increase/")
def increase_stock_endpoint(productid: int, amount: int, db: Session = Depends(get_db)):
    return increase_stock(productid, amount, db)

# Function to change the price of a product
def change_price(productid: int, new_price: float, db: Session):
    try:
        produkt = db.query(Store).filter(Store.productid == productid).first()
        if produkt is None:
            raise HTTPException(status_code=404, detail="Produkt not found")
        produkt.prize = new_price
        db.commit()
        logger.info("Changed price successfully", extra={"productid": productid, "new_price": new_price})
        return {"message": "Changed price successfully", "productid": productid, "new_price": new_price}
    except Exception as e:
        db.rollback()
        logger.error("Error changing price", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to change the price of a product
@router.post("/stock/change_price/")
def change_price_endpoint(productid: int, new_price: float, db: Session = Depends(get_db)):
    return change_price(productid, new_price, db)