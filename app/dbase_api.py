from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .logger_config import logger
import json

DATABASE_URL = "postgresql://user:your_password@127.0.0.1:5432/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise,
    # you will have to import them first before calling init_db()
    from . import models

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        Base.metadata.create_all(bind=engine)
        print("Database tables created.")
    else:
        print("Database tables already exist.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def delete_table(table_name: str):
    from .models import User, Card
    logger.info(f"Table delete_table for {table_name}")
    if table_name == "users":
        Base.metadata.drop_all(bind=engine, tables=[User.__table__])
    elif table_name == "cards":
        Base.metadata.drop_all(bind=engine, tables=[Card.__table__])
    else:
        raise ValueError("Invalid table name")
    print(f"Table {table_name} force deleted.")

def create_table(table_name: str):
    from .models import User, Card
    if table_name == "users":
        User.__table__.create(bind=engine)
    elif table_name == "cards":
        Card.__table__.create(bind=engine)
    else:
        raise ValueError("Invalid table name")
    print(f"Table {table_name} created.")

def recreate_table(table_name: str):
    delete_table(table_name)
    create_table(table_name)
    print(f"Table {table_name} recreated.")

def table_configuration(table_name: str):
    inspector = inspect(engine)
    print(f"table_configuration Table {table_name}.")
    indexes = inspector.get_indexes(table_name) or []
    print(f"table_configuration Indexes {indexes}.")

    config = {
        "indexes": [dict(index) for index in indexes]
    }

    logger.info(f"api Table configuration for {table_name}: {config}")
    retur = {"configuration": config}

    try:
        json.dumps(retur)
    except (TypeError, ValueError) as e:
        logger.error(f"Configuration for table {table_name} is not JSON serializable: {e}")
        raise ValueError(f"Configuration for table {table_name} is not JSON serializable: {e}")

    return retur