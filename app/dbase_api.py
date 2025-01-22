from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

def force_delete_table(table_name: str):
    with engine.connect() as connection:
        connection.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
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
    force_delete_table(table_name)
    create_table(table_name)
    print(f"Table {table_name} recreated.")

def check_table_configuration(table_name: str):
    inspector = inspect(engine)
    print(f"check_table_configuration Table {table_name}.")
    columns = inspector.get_columns(table_name) or []
    primary_keys = inspector.get_pk_constraint(table_name) or {}
    foreign_keys = inspector.get_foreign_keys(table_name) or []
    indexes = inspector.get_indexes(table_name) or []

    config = {
        "columns": [dict(column) for column in columns],
        "primary_keys": {key: (value if isinstance(value, list) else [value]) for key, value in primary_keys.items()} if primary_keys else {},
        "foreign_keys": [dict(fk) for fk in foreign_keys],
        "indexes": [dict(index) for index in indexes]
    }

    return config