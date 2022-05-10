from werkzeug import security
import jwt
from app.settings import configMap
from app import models
# import pymongo
import bson

#-------------------------------------------
def generate_password_hash(password:str):
  passwordHash = security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
  return passwordHash

#-----------------------
def check_password_hash(hash:str, password:str):
  res = security.check_password_hash(hash, password)
  return res

#-------------------------------------------
def encode_jwt(payload:dict):
  jwtStr = jwt.encode(payload, configMap.JWT_SECRET, algorithm=configMap.JWT_ALGO)
  return jwtStr

#-----------------------
def decode_jwt(jwt_str:str):
  payload = jwt.decode(jwt_str, configMap.JWT_SECRET, algorithms=configMap.JWT_ALGO)
  return payload

#-------------------------------------------
def remove_empty_strings_from_dict(item:dict):
  newItem = {}
  for key,val in item.items():
    if val == "":
      continue
    newItem[key] = val

  return newItem

#-------------------------------------------
def merge_dicts(a:dict, b:dict):
  for key,val in b.items():
    if val:
      a[key] = val
    # if val == "":
    #   del a[key]
  return a

#-------------------------------------------
def calc_image_size(width:int, height:int, thumb=False):

  curHeight = models.imageParas["maxImageHeigh"]
  if thumb:
    curHeight = models.imageParas["thumbHeight"]

  rel = width / height
  newWith = curHeight * rel

  return round(newWith), curHeight


#-------------------------------------------
#SCHROTT, get net
# def remove_objectids_from_dict(item:dict):
#   for key,val in item.items():
#     if str(type(val)) == 'bson.objectid.ObjectId':
#       item[key] = str(val)

#     return item


#-------------------------------------------

