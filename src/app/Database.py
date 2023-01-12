import os
from databases import Database
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
artifacts = Table(
    "artifacts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), unique=True),
    Column("element", String(255)),
    Column("level", Integer),
)

database = Database(DATABASE_URL)
