import os
# os.environ["INIT_ADMIN_USER"] = "palim"

from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, validator
import jwt
import time

from app import helpers, settings, tools

#-Build the App--------------------------------------
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#-Initial Fuctions for App Prep----------------------
tools.initialize_db()

#-Define the Data Models-----------------------------
class User(BaseModel):
  username: str
  role: str | None = None
  email: str | None = None
  full_name: str | None = None
  disabled: bool | None = None

  @validator('role')
  def check_role(cls, val):
    roleList = ["adminx", "user"]
    if val not in roleList:
      raise ValueError('must one of the following %s' %roleList)

    return val.title()

#-Auth Helper Functions------------------------------
def decode_token(token):
  dbRes = tools.get_user_by_token(token)

  res = User( 
    username = dbRes.get("username"), 
    role = dbRes.get("role"), 
    email= dbRes.get("email")
  )
  return res

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
  
  authRes = tools.check_auth(username=form_data.username, password=form_data.password)
  if not authRes:
    raise HTTPException(status_code=400, detail="Incorrect credentials")

  dbRes = tools.get_user_by_name(form_data.username) 
  nowMs = round(time.time())
  payload = {
    "username": dbRes["username"],
    "role": dbRes["role"],
    "created": nowMs,
    "expires": nowMs + ( settings.configMap.JWT_TOKEN_VALIDITY_TIME_IN_H * 60 * 60 * 1000 )
  }

  jwtStr = helpers.encode_jwt(payload=payload)
  return {"access_token": jwtStr, "token_type": "Bearer"}


#--------------------------------
@app.get("/users")
async def api_users_get(token: str = Depends(oauth2_scheme)) -> dict:
  return []

#--------------------------------
@app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#   return current_user

async def read_user_me( token: str = Depends(oauth2_scheme) ):
  dbRes = tools.get_user_by_token(token)

  res = User(username=dbRes["username"])
  for key,val in dbRes.items():
    setattr(res, key, val)

  return res

#--------------------------------


#----------------------------------------------------
