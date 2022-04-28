from shutil import ExecError
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

  if "password_hash" not in dbRes:
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
def check_admin_by_token(jwt_str):
  payload = helpers.decode_jwt(jwt_str) 
  if payload["role"] == "admin":
    return True
  else:
    return False

#--------------------------
def get_users_from_db():
  mongoDb = create_mongo_cli()
  qry = [ 
    { '$addFields': {'_id': { '$toString': '$_id' } }}, 
    { '$project': { 'password_hash': 0 } }
  ]
  dbRes = mongoDb.users.aggregate(qry)
  resList = []
  for item in dbRes:
    resList.append(item)

  return resList

#--------------------------
def get_list_of_usernames_from_db():
  mongoDb = create_mongo_cli()
  dbRes = mongoDb.users.find({}, {"username":1, "_id":0})
  resList = []
  for item in dbRes:
    resList.append(item["username"])

  return resList

#--------------------------
def add_user(item):
  userNames = get_list_of_usernames_from_db()
  if item["username"] in userNames:
    raise Exception("User '%s' already exists" %item["username"])
  
  mongoDb = create_mongo_cli()
  id = mongoDb.users.insert_one(item).inserted_id
  return str(id)

#--------------------------


#--------------------------


#--------------------------


#--------------------------


