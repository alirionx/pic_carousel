import os
# os.environ["INIT_ADMIN_USER"] = "palim"

from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, validator, constr, EmailStr, SecretStr
from typing import Literal
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
  username: constr(min_length=4)
  role: Literal["user", "admin", "disabled"]
  email: EmailStr
  firstname: str | None = None
  lastname: constr(min_length=2)

class UserPatch(BaseModel):
  username: constr(min_length=4)  | None = None
  role: Literal["user", "admin", "disabled"]  | None = None
  email: EmailStr | None = None
  firstname: str | None = None
  lastname: constr(min_length=2) | None = None

class Password(BaseModel):
  password: SecretStr

#-Auth Helper Functions------------------------------

def check_admin(token):
  chkAdmin = tools.check_admin_by_token(token)
  if not chkAdmin:
    raise HTTPException(status_code=400, detail="Must be admin")


#-The Routes-----------------------------------------
@app.get("/", tags=["root"])
async def api_root_get() -> dict:
  return {"message": "Welcome to the API of the Pic Carousel App"}


#--------------------------------------------
@app.post("/token", tags=["auth"])
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


#--------------------------------------------
@app.get("/users", tags=["users"])
async def api_users_get(token: str = Depends(oauth2_scheme)):
  check_admin(token)

  res = tools.get_users_from_db()
  return res


#--------------------------------------------
@app.post("/users", tags=["users"])
async def api_users_post(item: User, token: str = Depends(oauth2_scheme)):
  check_admin(token)

  item = item.dict(exclude_none=True, exclude_unset=True)
  try:
    id = tools.add_user(item)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return item


#--------------------------------------------
@app.get("/user/me", tags=["users"])
async def api_user_me_get(token: str = Depends(oauth2_scheme)):

  res = tools.get_user_by_token(token)
  return res


#--------------------------------------------
@app.get("/user/{username}", tags=["users"])
async def api_user_get(username, token: str = Depends(oauth2_scheme)):
  check_admin(token)

  res = tools.get_user_by_name(username)
  if not res:
    raise HTTPException(status_code=400, detail="User '%s' not found" %username)

  return res


#--------------------------------------------
@app.put("/user/{username}", tags=["users"])
async def api_user_put(item: User, username:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)

  usrDict = tools.get_user_by_name(username)
  if not usrDict:
    raise HTTPException(status_code=400, detail="User '%s' not found" %username)

  item = item.dict(exclude_none=True, exclude_unset=True)

  try:
    # res = tools.change_user_by_username(mergedDict)
    res = tools.replace_user_by_username(username, item)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
  
  return item


#--------------------------------------------
@app.patch("/user/{username}", tags=["users"])
async def api_user_patch(item: UserPatch, username:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)
  
  res = tools.get_user_by_name(username)
  if not res:
    raise HTTPException(status_code=404, detail="User '%s' not found" %username)
  
  existingItem = User(**res)
  newItem = item.dict(exclude_none=True, exclude_unset=True)
  updatedItem = existingItem.copy(update=newItem)
  
  dbItem = updatedItem.dict(exclude_none=True, exclude_unset=True)
  tools.replace_user_by_username(username, dbItem)

  return updatedItem


#--------------------------------------------
@app.delete("/user/{username}", tags=["users"])
async def api_user_delete(username:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)

  res = tools.delete_user_by_username(username=username)
  if not res :
    raise HTTPException(status_code=400, detail="User '%s' does not exist or faild to delete" %username)

  return {"username": username}  


#--------------------------------------------
@app.put("/user/password/{username}", tags=["users"])
async def api_user_patch(item: Password, username:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)

  password = item.password.get_secret_value()
  if len(password) < settings.configMap.MIN_PWD_LEN:
    raise HTTPException(status_code=400, detail="password to short")

  try:
    tools.set_user_password_hash(username=username, password=password)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return item


#--------------------------------------------


#--------------------------------------------


#--------------------------------------------



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
