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

class CreaseStockRequest(BaseModel):
    productid: int
    amount: int

class ChangePriceRequest(BaseModel):
    productid: int
    new_price: float

# Create a router for the cards endpoints
router = APIRouter()

# Lägg till en ny produkt 
@router.post("/stock/")
def add_produkt(stock: Inventory, db: Session = Depends(get_db)):
    try:
        print(f"Received stock type: {stock}")
        print(f"Received db type: {type(db)}")
        print(f"stock.prodname type: {type(stock.prodname)}")
        print(f"stock.productid type: {type(stock.productid)}")
        print(f"stock.instock type: {type(stock.instock)}")
        print(f"stock.prize type: {type(stock.prize)}")

        existing_product = db.query(Store).filter(Store.productid == stock.productid).first()
        if existing_product:
            raise HTTPException(status_code=400, detail={"message": "Product already exists", "produkt": existing_product})

        new_produkt = Store(prodname=stock.prodname, productid=stock.productid, instock=stock.instock, prize=stock.prize)
        db.add(new_produkt)
        db.commit()
        db.refresh(new_produkt)
        logger.info(f"User produkt successfully {new_produkt}")
        return {"message": "User produkt successfully", "produkt": new_produkt}
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
        logger.info("Produkt deleted successfully", extra={"prod_id": productid})
        return {"message": "Produkt deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting produkt", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to list all product IDs
@router.get("/stock/productids/")
def list_all_productids(db: Session = Depends(get_db)):
    try:
        productids = db.query(Store.productid).all()
        logger.info(f"Fetched all product IDs {productids}")
        return {"productids": [pid[0] for pid in productids]}
    except Exception as e:
        logger.error("Error fetching product IDs", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to check if a product ID exists
@router.get("/stock/productid_exists/{productid}")
def do_productid_exist(productid: int, db: Session = Depends(get_db)):
    try:
        exists = db.query(Store).filter(Store.productid == productid).first() is not None
        logger.info(f"Checked existence of product ID {productid}: {exists}")
        return {"productid": productid, "exists": exists}
    except Exception as e:
        logger.error("Error checking product ID existence", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to decrease the stock of a product
@router.post("/stock/decrease/")
def decrease_stock(request: CreaseStockRequest, db: Session = Depends(get_db)):
    try:
        produkt = db.query(Store).filter(Store.productid == request.productid).first()
        if produkt is None:
            raise HTTPException(status_code=404, detail="Produkt not found")
        if produkt.instock < request.amount:
            raise HTTPException(status_code=406, detail="Not enough stock")
        produkt.instock -= request.amount
        db.commit()
        logger.info("Decreased stock successfully", extra={"productid": request.productid, "amount": request.amount})
        return {"message": "Decreased stock successfully", "productid": request.productid, "new_stock": produkt.instock}
    except Exception as e:
        db.rollback()
        logger.error("Error decreasing stock", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Function to increase the stock of a product
@router.post("/stock/increase/")
def increase_stock(request: CreaseStockRequest, db: Session = Depends(get_db)):
    try:
        produkt = db.query(Store).filter(Store.productid == request.productid).first()
        print(f"increase_stock produkt: {produkt}")
        if produkt is None:
            logger.error(f"Increased stock produkt dont exist {request.productid}")
            raise HTTPException(status_code=404, detail="Produkt not found")
        produkt.instock += request.amount
        logger.info(f"Increased stock new stock {produkt.instock}")
        db.commit()
        logger.info(f"Increased stock successfully {request.productid} {request.amount}")
        return {"message": "Increased stock successfully", "productid": request.productid, "new_stock": produkt.instock}
    except Exception as e:
        db.rollback()
        logger.error(f"Error increasing stock {request.productid} {request.amount}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Function to change the price of a product
@router.post("/stock/change_price/")
def change_price(request: ChangePriceRequest, db: Session = Depends(get_db)):
    try:
        produkt = db.query(Store).filter(Store.productid == request.productid).first()
        if produkt is None:
            raise HTTPException(status_code=404, detail="Produkt not found")
        produkt.prize = request.new_price
        db.commit()
        logger.info(f"Changed price successfully {request.productid} {request.new_price}")
        return {"message": "Changed price successfully", "productid": request.productid, "new_price": request.new_price}
    except Exception as e:
        db.rollback()
        logger.error("Error changing price", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to get the stock of a product
@router.get("/stock/{productid}/instock")
def get_instock(productid: int, db: Session = Depends(get_db)):
    try:
        produkt = db.query(Store).filter(Store.productid == productid).first()
        if produkt is None:
            raise HTTPException(status_code=404, detail="Produkt not found")
        return {"productid": productid, "instock": produkt.instock}
    except Exception as e:
        logger.error("Error fetching instock", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
