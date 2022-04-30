import time
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
    usrDict = {
      "username": configMap.INIT_ADMIN_USER,
      "role": "admin"
    }
    userId = mongoDb.users.insert_one(usrDict).inserted_id
    
    pwdHash = helpers.generate_password_hash(configMap.INIT_ADMIN_PASSWORD)
    hashDict = {
      "user_id": userId,
      "password_hash": pwdHash
    }
    mongoDb.hashes.insert_one(hashDict)
  

#--------------------------
def check_auth(username:str, password:str ):
  mongoDb = create_mongo_cli()
  # dbRes = mongoDb.users.find_one({"username": username})
  
  dbRes = mongoDb.users.aggregate([
    {
        '$match': {
            'username': username
        }
    }, {
        '$lookup': {
            'from': 'hashes', 
            'localField': '_id', 
            'foreignField': 'user_id', 
            'as': 'item'
        }
    }, {
        '$addFields': {
            'password_hash': {
                '$first': '$item.password_hash'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'password_hash': 1
        }
    }
  ])
  resList = list(dbRes)
  if not len(resList):
    return False
    
  password_hash = resList[0]["password_hash"]
  authRes = helpers.check_password_hash(hash=password_hash, password=password)
  return authRes 

#--------------------------
def get_user_by_name(username):
  mongoDb = create_mongo_cli()
  dbRes = mongoDb.users.find_one( {"username": username}, {"_id":0} )
  return dbRes

#--------------------------
def get_user_by_token(jwt_str):
  payload = helpers.decode_jwt(jwt_str) 

  mongoDb = create_mongo_cli()
  dbRes = mongoDb.users.find_one( {"username": payload["username"]}, {"_id":0} )
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
    { '$project': { 'password_hash': 0, "_id": 0 } }
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
def add_user(item:dict):
  userNames = get_list_of_usernames_from_db()
  if item["username"] in userNames:
    raise Exception("User '%s' already exists" %item["username"])
  
  mongoDb = create_mongo_cli()
  id = mongoDb.users.insert_one(dict(item)).inserted_id
  return str(id)

#--------------------------
def change_user_by_username(item):
  userName = item["username"]
  mongoDb = create_mongo_cli()

  qry = {"username": userName}
  newVals = { "$set": item }
  mongoDb.users.update_one(qry, newVals)
  
  return item

#--------------------------
def replace_user_by_username(username, item):
  mongoDb = create_mongo_cli()

  qry = {"username": username}
  mongoDb.users.replace_one(qry, item)
  
  return item

#--------------------------
def set_user_password_hash(username, password):
  mongoDb = create_mongo_cli()

  chk = mongoDb.users.find_one( {"username": username}, {"_id":1} )
  if not chk:
    raise Exception("user '%s' does not exist" %username)
  id = str(chk["_id"])
  hash = helpers.generate_password_hash(password)

  item = {
    "timestamp" :round(time.time()),
    "user_id": id,
    "password_hash": hash
  }

  mongoDb.hashes.delete_one({"user_id": id})
  mongoDb.hashes.insert_one(item)

#--------------------------


#--------------------------


#--------------------------


