from werkzeug import security
import jwt
from app.settings import configMap

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

