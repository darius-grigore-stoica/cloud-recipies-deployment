"""
main.py — The entry point of the FastAPI application.
"""
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import recipes

# Create all database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe Sharing App", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# No static files mount needed — all CSS/JS is inside index.html
templates = Jinja2Templates(directory="templates")

app.include_router(recipes.router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/recipe/{recipe_id}")
def recipe_detail(request: Request, recipe_id: int):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/add")
def add_recipe(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}