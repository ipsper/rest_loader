from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from .logger_config import logger
from .dbase_api import get_db, engine, force_delete_table, create_table, recreate_table, check_table_configuration

# Create a router for the cards endpoints
router = APIRouter()

class TableName(BaseModel):
    table_name: str

# Endpoint to get all table names
@router.get("/tables/")
def get_table_names(db: Session = Depends(get_db)):
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info("Fetched all table names")
        return {"tables": tables}
    except Exception as e:
        logger.error("Error fetching table names", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to delete a table
@router.delete("/tables/")
def delete_table(table: TableName, db: Session = Depends(get_db)):
    try:
        force_delete_table(table.table_name)
        db.commit()
        logger.info("Table deleted successfully", extra={"table_name": table.table_name})
        return {"message": f"Table {table.table_name} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting table", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to delete and recreate a table
@router.post("/tables/recreate/")
def recreate_table_endpoint(table: TableName, db: Session = Depends(get_db)):
    try:
        recreate_table(table.table_name)
        db.commit()
        logger.info("Table recreated successfully", extra={"table_name": table.table_name})
        return {"message": f"Table {table.table_name} recreated successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Error recreating table", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to create a table based on User or Card class
@router.post("/tables/create/")
def create_table_endpoint(table: TableName, db: Session = Depends(get_db)):
    try:
        create_table(table.table_name)
        logger.info("Table created successfully", extra={"table_name": table.table_name})
        return {"message": f"Table {table.table_name} created successfully"}
    except Exception as e:
        logger.error("Error creating table", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to check table configuration
@router.post("/tables/configuration/")
def check_table_configuration_endpoint(table: TableName, db: Session = Depends(get_db)):
    try:
        config = check_table_configuration(table.table_name)
        logger.info("Fetched table configuration", extra={"table_name": table.table_name})
        return {"configuration": config}
    except Exception as e:
        logger.error("Error fetching table configuration", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
