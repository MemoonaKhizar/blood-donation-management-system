from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.routes import auth_router
from database import Base, engine
from auth import models

# Initialize FastAPI app
app = FastAPI()

# Mount static directory (for CSS, images, JS if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template directory
templates = Jinja2Templates(directory="templates")

# Include authentication routes
app.include_router(auth_router)

# Create all database tables
Base.metadata.create_all(bind=engine)
