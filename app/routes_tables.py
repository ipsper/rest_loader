from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from .logger_config import logger
from .dbase_api import get_db, engine, delete_table, create_table as db_create_table, recreate_table, table_configuration

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
        logger.error(f"Error fetching table names")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to delete a table
@router.delete("/tables/")
def delete_table(table: TableName, db: Session = Depends(get_db)):
    try:
        back = delete_table(table.table_name)
        logger.info(f"Table delete back {back}")
        db.commit()
        logger.info(f"Table deleted successfully {table.table_name}")
        return {"message": f"Table {table.table_name} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting table {table.table_name}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to delete and recreate a table
@router.post("/tables/recreate/")
def recreate_table(table: TableName, db: Session = Depends(get_db)):
    try:
        back = recreate_table(table.table_name)
        logger.info(f"Table recreate back {back}")

        db.commit()
        logger.info(f"Table recreated successfully  {table.table_name}")
        return {"message": f"Table {table.table_name} recreated successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error recreating table {table.table_name}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to create a table based on User or Card class
@router.post("/tables/create/")
def create_table(table: TableName, db: Session = Depends(get_db)):
    try:
        db_create_table(table.table_name)
        logger.info(f"Table created successfully {table.table_name}")
        return {"message": f"Table {table.table_name} created successfully"}
    except Exception as e:
        logger.error(f"Error creating table {table.table_name}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint to check table configuration
@router.post("/tables/configuration/")
def check_table_configuration(table: TableName, db: Session = Depends(get_db)):
    try:
        config = table_configuration(table.table_name)
        logger.info(f"Table configuration for {table.table_name} : {config}")
        return config
    except Exception as e:
        logger.error(f"Error fetching table configuration {table.table_name}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
