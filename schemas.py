"""
schemas.py — Pydantic models that validate incoming request data
and shape outgoing response data. Separate from DB models.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RecipeBase(BaseModel):
    title:       str
    description: Optional[str] = None
    ingredients: str            # newline-separated
    steps:       str            # newline-separated
    category:    Optional[str] = None
    prep_time:   Optional[int] = None
    cook_time:   Optional[int] = None
    servings:    Optional[int] = None
    author:      Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeOut(RecipeBase):
    id:         int
    image_url:  Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # lets Pydantic read SQLAlchemy model fields
