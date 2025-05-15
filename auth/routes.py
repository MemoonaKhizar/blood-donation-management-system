from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from auth.schemas import UserCreate, UserLogin
from auth.models import User
from auth.utils import hash_password, verify_password, create_access_token
from database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

templates = Jinja2Templates(directory="templates")
auth_router = APIRouter()

@auth_router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@auth_router.post("/register")
def register(email: str = Form(...), username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = User(email=email, username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=302)

@auth_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        return {"error": "Invalid credentials"}
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
