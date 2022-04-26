from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt

from app import settings

#-Build the App--------------------------------------
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#-Define the Data Models-----------------------------
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

#-Auth Helper Functions------------------------------
def decode_token(token):
  return User( 
    username=token + "fakedecoded", 
    email="john@example.com", 
    full_name="John Doe"
  )
async def get_current_user(token: str = Depends(oauth2_scheme)):
  user = decode_token(token)
  return user

#-The Routes-----------------------------------------
@app.get("/", tags=["root"])
async def api_root_get() -> dict:
  return {"message": "Welcome to the API of the Pic Carousel App"}

#--------------------------------
@app.post("/token")
async def api_token_post(form_data: OAuth2PasswordRequestForm = Depends()):
  payload = {
    "username": form_data.username,
    "role": "masterChief"
  }
  encoded_jwt = jwt.encode(payload, settings.env_data_map["jwt_secret"], algorithm=settings.env_data_map["jwt_algo"])
  
  return {"access_token": encoded_jwt, "token_type": "Bearer"}


#--------------------------------
@app.get("/users")
async def api_users_get(token: str = Depends(oauth2_scheme)) -> dict:
  return []

#--------------------------------
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
  return current_user

#--------------------------------


#----------------------------------------------------
