"""
main.py — The entry point of the FastAPI application.
Run locally with: uvicorn main:app --reload
Azure App Service will also use this file.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import recipes

# ── Create all database tables on startup (if they don't exist) ───────────────
# This is safe to run repeatedly — it won't delete existing data
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe Sharing App", version="1.0.0")

# ── Allow browser requests from any origin (needed for JS fetch calls) ────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files (CSS, JS, images) and HTML templates ────────────────────────
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory="templates")

# ── Include the recipes API router ────────────────────────────────────────────
app.include_router(recipes.router)


# ── Serve the frontend (single-page app pattern) ─────────────────────────────
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/recipe/{recipe_id}")
def recipe_detail(request: Request, recipe_id: int):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/add")
def add_recipe(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ── Health check endpoint (Azure uses this to verify the app is running) ──────
@app.get("/health")
def health():
    return {"status": "ok"}
