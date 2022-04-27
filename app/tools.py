import pymongo
from app.settings import configMap
import app.helpers as helpers

#--------------------------
def create_mongo_cli():
  mongoCli = pymongo.MongoClient("mongodb://%s:%s/" %(configMap.MONGODB_HOST, configMap.MONGODB_PORT))
  mongoDb = mongoCli[configMap.MONGODB_DBNAME]
  return mongoDb

#--------------------------
def initialize_db():
  mongoDb = create_mongo_cli()
  res = mongoDb.users.find()
  if not len(list(res)):
    pwdHash = helpers.generate_password_hash(configMap.INIT_ADMIN_PASSWORD)
    usrDict = {
      "username": configMap.INIT_ADMIN_USER,
      "password_hash": pwdHash,
      "role": "admin"
    }
    mongoDb.users.insert_one(usrDict)
    
#--------------------------
def check_auth(username:str, password:str ):
  mongoDb = create_mongo_cli()
  dbRes = mongoDb.users.find_one({"username": username})
  if not dbRes:
    return False

  password_hash = dbRes["password_hash"]
  authRes = helpers.check_password_hash(hash=password_hash, password=password)
  return authRes 

#--------------------------
def get_user_by_name(username):
  mongoDb = create_mongo_cli()
  dbRes = mongoDb.users.find_one( {"username": username}, {"_id":0, "password_hash":0} )
  return dbRes

#--------------------------
def get_user_by_token(jwt_str):
  payload = helpers.decode_jwt(jwt_str) 

  mongoDb = create_mongo_cli()
  dbRes = mongoDb.users.find_one( {"username": payload["username"]}, {"_id":0, "password_hash":0} )
  return dbRes

#--------------------------


