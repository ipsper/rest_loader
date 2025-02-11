from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .logger_config import logger
from .models import Produkt
from .dbase_api import get_db

# Pydantic model for the request body
class DoProdukt(BaseModel):
    productid: str
    weight: str
    volym: str
    produktionstid: str
    tillverkare: str

# Create a router for the cards endpoints
router = APIRouter()

# skapa en produkt
@router.post("/product/")
def do_product(product: DoProdukt, db: Session = Depends(get_db)):
    try:
        new_product = Produkt(productid=product.productid, weight=product.weight, volym=product.volym,
                             produktionstid=product.produktionstid, tillverkare=product.tillverkare)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        logger.info(f"Added a product successfullyproductid: {new_product.productid}")
        return {"message": "added product successfully", "product": new_product}
    except Exception as e:
        db.rollback()
        logger.error("Error added a product", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Läs alla produkter  från databasen
@router.get("/product/")
def read_products(db: Session = Depends(get_db)):
    try:
        purchase = db.query(Produkt).all()
        logger.info("Fetched all products")
        return {"products": purchase}
    except Exception as e:
        logger.error("Error fetching products", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Ta bort ett köp baserat på ID
@router.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Produkt).filter(Produkt.id == id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="product not found")
        db.delete(product)
        db.commit()
        logger.info("product deleted successfully", extra={"product id": id})
        return {"message": "product deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting product", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")