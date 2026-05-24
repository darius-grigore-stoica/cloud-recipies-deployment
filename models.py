"""
models.py — Defines the database tables using SQLAlchemy ORM.
Each class = one table in Azure SQL Database.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=False)   # stored as newline-separated text
    steps       = Column(Text, nullable=False)   # stored as newline-separated text
    category    = Column(String(100), nullable=True)
    prep_time   = Column(Integer, nullable=True)  # minutes
    cook_time   = Column(Integer, nullable=True)  # minutes
    servings    = Column(Integer, nullable=True)
    image_url   = Column(String(500), nullable=True)  # points to Azure Blob Storage
    author      = Column(String(100), nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())
