import base64
import os
# os.environ["INIT_ADMIN_USER"] = "palim"

from fastapi import FastAPI, Request, status, HTTPException, UploadFile, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse

from io import BytesIO
import jwt
import time

from app import helpers, settings, tools
from app.models import User, UserPatch, UserMe, Password, Carousel
from app.models import imageTypesCompression, allowedImageLength

#-Build the App-------------------------------------------------
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#-Initial Fuctions for App Prep---------------------------------
tools.initialize_db()


#-Auth Helper Functions-----------------------------------------

def check_admin(token):
  chkAdmin = tools.check_admin_by_token(token)
  if not chkAdmin:
    raise HTTPException(status_code=400, detail="Must be admin")


#-The Routes----------------------------------------------------
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
    res = tools.add_user(item)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return res


#--------------------------------------------
@app.get("/user/me", tags=["users"])
async def api_user_me_get(token: str = Depends(oauth2_scheme)):

  res = tools.get_user_by_token(token)
  return res


#--------------------------------------------
@app.get("/user/{id}", tags=["users"])
async def api_user_get(id:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)

  res = tools.get_user_by_id(id=id)
  if not res:
    raise HTTPException(status_code=400, detail="User '%s' not found" %id)

  return res

#--------------------------------------------
@app.put("/user/me", tags=["users"])
async def api_me_put(item: UserMe, token:str = Depends(oauth2_scheme)):
  
  res = tools.get_user_by_token(jwt_str=token)
  id = res["_id"]
  
  existingItem = User(**res)
  newItem = item.dict(exclude_none=True, exclude_unset=True)
  updatedItem = existingItem.copy(update=newItem)
  dbItem = updatedItem.dict(exclude_none=True, exclude_unset=True)
  
  try:
    res = tools.replace_user_by_id(id, dbItem)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
  
  return res


#--------------------------------------------
@app.put("/user/{id}", tags=["users"])
async def api_user_put(item: User, id:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)

  usrDict = tools.get_user_by_id(id)
  if not usrDict:
    raise HTTPException(status_code=400, detail="User '%s' not found" %id)

  item = item.dict(exclude_none=True, exclude_unset=True)

  try:
    # res = tools.change_user_by_username(mergedDict)
    res = tools.replace_user_by_id(id, item)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
  
  return res


#--------------------------------------------
@app.patch("/user/{id}", tags=["users"])
async def api_user_patch(item: UserPatch, id:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)
  
  res = tools.get_user_by_id(id)
  if not res:
    raise HTTPException(status_code=404, detail="User '%s' not found" %id)
  
  existingItem = User(**res)
  newItem = item.dict(exclude_none=True, exclude_unset=True)
  updatedItem = existingItem.copy(update=newItem)
  
  dbItem = updatedItem.dict(exclude_none=True, exclude_unset=True)
  item = tools.replace_user_by_id(id, dbItem)

  return item


#--------------------------------------------
@app.delete("/user/{id}", tags=["users"])
async def api_user_delete(id:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)

  res = tools.delete_user_by_id(id=id)
  if not res :
    raise HTTPException(status_code=400, detail="User '%s' does not exist or faild to delete" %id)

  return {"_id": id}  


#--------------------------------------------
@app.put("/user/password/me", tags=["users"])
async def api_user_patch(item: Password, token:str = Depends(oauth2_scheme)):

  res = tools.get_user_by_token(jwt_str=token)
  id = res["_id"]

  password = item.password.get_secret_value()
  if len(password) < settings.configMap.MIN_PWD_LEN:
    raise HTTPException(status_code=400, detail="password to short")

  try:
    tools.set_user_password_hash(id=id, password=password)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return item


#--------------------------------------------
@app.put("/user/password/{id}", tags=["users"])
async def api_user_patch(item: Password, id:str, token:str = Depends(oauth2_scheme)):
  check_admin(token)

  password = item.password.get_secret_value()
  if len(password) < settings.configMap.MIN_PWD_LEN:
    raise HTTPException(status_code=400, detail="password to short")

  try:
    tools.set_user_password_hash(id=id, password=password)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return item


#--------------------------------------------
@app.get("/carousels", tags=["carousels"])
async def api_carousels_get(token:str = Depends(oauth2_scheme)):
  id = tools.get_user_by_token(token)["_id"]
  res = tools.get_carousels(id=id)
  return res

#-----------------------
@app.post("/carousels", tags=["carousels"])
async def api_carousels_post(item:Carousel, token:str = Depends(oauth2_scheme)):
  
  user_id = tools.get_user_by_token(token)["_id"]
  item = item.dict(exclude_none=True, exclude_unset=True)

  try:
    res = tools.add_carousel(item=item, user_id=user_id)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return res

#-----------------------
@app.put("/carousels/{id}", tags=["carousels"])
async def api_carousels_put(id:str, item:Carousel, token:str = Depends(oauth2_scheme)):
  
  user_id = tools.get_user_by_token(token)["_id"]
  item = item.dict(exclude_none=True, exclude_unset=True)

  chk = tools.check_carousel_owner(user_id=user_id, id=id)
  if not chk:
    raise HTTPException(status_code=400, detail="carousel not found or not owned by you")

  try:
    res = tools.replace_carousel_by_id(id=id, user_id=user_id, item=item)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return res

#--------------------------------------------
@app.get("/images", tags=["images"])
async def api_images_get(token:str = Depends(oauth2_scheme)):
  
  user_id = tools.get_user_by_token(token)["_id"]
  res = tools.get_images(user_id=user_id)
  return res


#-------------
@app.get("/thumbs", tags=["images"])
async def api_thumbs_get(token:str = Depends(oauth2_scheme)):
  
  user_id = tools.get_user_by_token(token)["_id"]
  res = tools.get_images(user_id=user_id, thumbs=True)
  return res

#--------------------------------------------
@app.post("/image", tags=["images"])
async def api_image_post(file: UploadFile, token:str = Depends(oauth2_scheme)):
  
  if file.content_type not in imageTypesCompression.keys():
    raise HTTPException(status_code=400, detail="invalid file type. Please use '%s'" %imageTypesCompression.keys())

  res = tools.get_user_by_token(token) 
  username = res["username"]
  res = await tools.add_image(file=file, username=username)
  
  return res

#--------------------------------------------
@app.get("/stream/{id}", tags=["images"])
async def api_stream_get(id:str, token:str = Depends(oauth2_scheme)):

  try:
    user_id = tools.get_user_by_token(token)["_id"]
    res, contentType = await tools.get_image_byte(id=id, user_id=user_id)
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

  return StreamingResponse(BytesIO(res), media_type=contentType)

#--------------------------------------------



#-TEST AREA------------------------------------------

#--------------------------------


#--------------------------------


#----------------------------------------------------
