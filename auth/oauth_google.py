from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth.models import User
from database import get_db
from auth.utils import create_access_token
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth/google")
oauth = OAuth()

# Configure Google OAuth client
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Step 1: Redirect user to Google Login
@router.get("/")
async def login_with_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Step 2: Callback from Google
@router.get("/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    email = user_info.get("email")
    username = user_info.get("name")

    # Check if user already exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Register new user
        user = User(
            email=email,
            username=username,
            hashed_password="",  # No password for Google users
            is_verified=True,
            is_google_account=True
        )
        db.add(user)
        db.commit()

    # Generate JWT Token
    jwt_token = create_access_token({"sub": email})
    response = RedirectResponse(url="/welcome")  # Update as needed
    response.set_cookie("access_token", jwt_token)
    return response
