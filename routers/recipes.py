"""
routers/recipes.py — All the API endpoints for recipes.
Each function handles one type of request (GET, POST, PUT, DELETE).
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas
from database import get_db
from blob_storage import upload_image, delete_image

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


# ── GET all recipes (with optional category filter) ───────────────────────────
@router.get("/", response_model=List[schemas.RecipeOut])
def get_recipes(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Recipe)
    if category:
        query = query.filter(models.Recipe.category == category)
    return query.order_by(models.Recipe.created_at.desc()).all()


# ── GET a single recipe by id ─────────────────────────────────────────────────
@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# ── POST create a new recipe (with optional image upload) ─────────────────────
@router.post("/", response_model=schemas.RecipeOut, status_code=201)
async def create_recipe(
    title:       str           = Form(...),
    description: Optional[str] = Form(None),
    ingredients: str           = Form(...),
    steps:       str           = Form(...),
    category:    Optional[str] = Form(None),
    prep_time:   Optional[int] = Form(None),
    cook_time:   Optional[int] = Form(None),
    servings:    Optional[int] = Form(None),
    author:      Optional[str] = Form(None),
    image:       Optional[UploadFile] = File(None),
    db:          Session       = Depends(get_db),
):
    image_url = None

    # If an image was uploaded, send it to Azure Blob Storage
    if image and image.filename:
        file_bytes = await image.read()
        image_url  = upload_image(file_bytes, image.filename, image.content_type)

    recipe = models.Recipe(
        title=title, description=description, ingredients=ingredients,
        steps=steps, category=category, prep_time=prep_time,
        cook_time=cook_time, servings=servings, author=author,
        image_url=image_url,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


# ── PUT update a recipe ───────────────────────────────────────────────────────
@router.put("/{recipe_id}", response_model=schemas.RecipeOut)
async def update_recipe(
    recipe_id:   int,
    title:       str           = Form(...),
    description: Optional[str] = Form(None),
    ingredients: str           = Form(...),
    steps:       str           = Form(...),
    category:    Optional[str] = Form(None),
    prep_time:   Optional[int] = Form(None),
    cook_time:   Optional[int] = Form(None),
    servings:    Optional[int] = Form(None),
    author:      Optional[str] = Form(None),
    image:       Optional[UploadFile] = File(None),
    db:          Session       = Depends(get_db),
):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Replace the image if a new one was uploaded
    if image and image.filename:
        delete_image(recipe.image_url)           # remove old image from Blob Storage
        file_bytes     = await image.read()
        recipe.image_url = upload_image(file_bytes, image.filename, image.content_type)

    recipe.title       = title
    recipe.description = description
    recipe.ingredients = ingredients
    recipe.steps       = steps
    recipe.category    = category
    recipe.prep_time   = prep_time
    recipe.cook_time   = cook_time
    recipe.servings    = servings
    recipe.author      = author

    db.commit()
    db.refresh(recipe)
    return recipe


# ── DELETE a recipe ───────────────────────────────────────────────────────────
@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    delete_image(recipe.image_url)
    db.delete(recipe)
    db.commit()
