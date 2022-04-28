import os
# os.environ["INIT_ADMIN_USER"] = "palim"

from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, validator, EmailStr
from typing import Literal, List
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
  _id: str | None = None
  username: str
  role: Literal["user", "admin", "disabled"]
  email: EmailStr
  firstname: str | None = None
  lastname: str


#-Auth Helper Functions------------------------------

def check_admin(token):
  chkAdmin = tools.check_admin_by_token(token)
  if not chkAdmin:
    raise HTTPException(status_code=400, detail="Must be admin")


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
async def api_users_get(token: str = Depends(oauth2_scheme)):
  check_admin(token)

  res = tools.get_users_from_db()
  return res

#--------------------------------
@app.post("/users")
async def api_users_post(item: User, token: str = Depends(oauth2_scheme)):
  check_admin(token)

  dictData = dict(item)
  try:
    id = tools.add_user(dictData)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  dictData["_id"] = id
  return dictData

#--------------------------------
@app.get("/user/me")
async def api_user_me_get(token: str = Depends(oauth2_scheme)):

  res = tools.get_user_by_token(token)
  return res

#--------------------------------
@app.get("/user/{username}")
async def api_user_get(username, token: str = Depends(oauth2_scheme)):
  check_admin(token)

  res = tools.get_user_by_name(username)
  if not res:
    raise HTTPException(status_code=400, detail="User '%s' not found" %username)

  return res

#--------------------------------


#--------------------------------







#-TEST AREA
#--------------------------------
# @app.get("/users/me")
# # async def read_users_me(current_user: User = Depends(get_current_user)):
# #   return current_user

# async def read_user_me( token: str = Depends(oauth2_scheme) ):
#   dbRes = tools.get_user_by_token(token)

#   res = User(username=dbRes["username"])
#   for key,val in dbRes.items():
#     setattr(res, key, val)

#   return res

#--------------------------------


#----------------------------------------------------
