import time
import pymongo
from bson import ObjectId
import gridfs
from app import models, settings
from app.settings import configMap
import app.helpers as helpers

from PIL import Image
from io import BytesIO, StringIO

#--------------------------------------------------------------------
def create_mongo_cli(cli_only=False):
  mongoCli = pymongo.MongoClient("mongodb://%s:%s/" %(configMap.MONGODB_HOST, configMap.MONGODB_PORT))
  if cli_only:
    return mongoCli
  mongoDb = mongoCli[configMap.MONGODB_DBNAME]
  return mongoDb

#--------------------------
def create_gridfs_cli():
  mongoCli = pymongo.MongoClient("mongodb://%s:%s/" %(configMap.MONGODB_HOST, configMap.MONGODB_PORT))
  mongoDb = mongoCli[configMap.MONGODB_GRIDFSDB]
  gridFsCli =  gridfs.GridFS(mongoDb)
  return gridFsCli

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
      "user_id": ObjectId(userId),
      "password_hash": pwdHash
    }
    mongoDb.hashes.insert_one(hashDict)
  

#--------------------------------------------------------------------
def check_auth(username:str, password:str ):
  mongoDb = create_mongo_cli()
  # dbRes = mongoDb.users.find_one({"username": username})
  
  dbRes = mongoDb.users.find_one({"username": username}, {"_id": 1})
  if not dbRes: return False

  userId = dbRes["_id"]
  dbRes = mongoDb.hashes.find_one({"user_id": userId}, {"_id": 0, "password_hash":1})
  if not dbRes: return False

  password_hash = dbRes["password_hash"]
  authRes = helpers.check_password_hash(hash=password_hash, password=password)
  return authRes 

#--------------------------
def get_user_by_name(username, object_id=False):
  mongoDb = create_mongo_cli()
  dbRes = mongoDb.users.find_one( {"username": username}, {"_id":object_id} )
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
  return list(dbRes)

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
def delete_user_by_username(username):
  mongoDb = create_mongo_cli()

  res = mongoDb.users.find_one({"username":username}, {"_id": 1})
  if not res : return False 
  userId = str(res["_id"])

  res = mongoDb.users.delete_one({"username":username}).deleted_count
  mongoDb.hashes.delete_one({"user_id":userId})
  
  return res

#--------------------------
def set_user_password_hash(username, password):
  mongoDb = create_mongo_cli()

  chk = mongoDb.users.find_one( {"username": username}, {"_id":1} )
  if not chk:
    raise Exception("user '%s' does not exist" %username)
  id = chk["_id"]
  hash = helpers.generate_password_hash(password)

  item = {
    "timestamp" :round(time.time()),
    "user_id": id,
    "password_hash": hash
  }

  mongoDb.hashes.delete_one({"user_id": id})
  mongoDb.hashes.insert_one(item)

#--------------------------------------------------------------------
#--- EinTraum in Code ;) ---#
async def add_image(file, username:str):
  userId = get_user_by_name(username=username, object_id=1)["_id"]
  data = await file.read()
  imageData = Image.open(BytesIO(data))
  imageFormat = file.content_type.split("/")[1]

  # Warum ich das nicht in eine Schleife packen kann, ist mir unklar....
  # Wenn ich das mache, schreibt er nen Nuller in GridFS... Wird evtl. an Async oder Byteio liegen..  

  curWith, curHeight = imageData.size
  newImageWith, newImageHeight = helpers.calc_image_size(curWith, curHeight)
  newThumbWith, newThumbHeight = helpers.calc_image_size(curWith, curHeight, thumb=True)
  
  newImageObj = imageData.resize((newImageWith, newImageHeight))
  newThumbObj = imageData.resize((newThumbWith, newThumbHeight))
  
  imageBuffer = BytesIO()
  thumbBuffer = BytesIO()
  
  newImageObj.save(imageBuffer, format=imageFormat, optimize=True, quality=models.imageTypesCompression[file.content_type])
  imageBuffer.seek(0)
  newThumbObj.save(thumbBuffer, format=imageFormat, optimize=True, quality=models.imageTypesCompression[file.content_type])
  thumbBuffer.seek(0)

  gridFsCli = create_gridfs_cli()
  image_id = gridFsCli.put(
    imageBuffer, 
    filename=file.filename, 
    contentType=file.content_type, 
    type="image", 
    user_id=userId 
  )
  gridFsCli.put(
    thumbBuffer, 
    filename=file.filename, 
    contentType=file.content_type, 
    type="thumb", 
    image_id=image_id,
    user_id=userId 
  )
  
  return True
  
#--------------------------
def get_images(username:str, thumbs=False):
  imgType = "image"
  if thumbs: imgType = "thumb"

  userId = get_user_by_name(username=username, object_id=1)["_id"]

  mongoCli = create_mongo_cli(cli_only=True)
  mongoDb = mongoCli[configMap.MONGODB_GRIDFSDB]
  
  res = mongoDb["fs.files"].aggregate([
    {
      '$match': { 'user_id': userId, "type": imgType }
    }, 
    {
      '$addFields': {
        'id': {'$toString': '$_id'}
      }
    }, 
    {
      '$project': {'user_id': 0, '_id': 0 }
    }
  ])

  return list(res)

#--------------------------
async def get_image_byte(id:str, username:str):
  
  picId = ObjectId(id)
  userId = get_user_by_name(username=username, object_id=1)["_id"]

  mongoCli = create_mongo_cli(cli_only=True)
  mongoDb = mongoCli[configMap.MONGODB_GRIDFSDB]
  chk = mongoDb["fs.files"].find_one({"user_id": userId, "_id": picId})
  if not chk:
    raise Exception("Image with id '%s' not found or not allowed" %id)
  else:
    contentType = chk["contentType"]
  
  gridFsCli = create_gridfs_cli()
  # data = gridFsCli.find_one({"_id": ObjectId(id)},no_cursor_timeout=True)
  res = gridFsCli.get(ObjectId(id)).read()

  return res, contentType

#--------------------------
def delete_image_by_id(id:str, username:str):
  picId = ObjectId(id)
  userId = get_user_by_name(username=username, object_id=1)["_id"]

  mongoCli = create_mongo_cli(cli_only=True)
  mongoDb = mongoCli[configMap.MONGODB_GRIDFSDB]
  res = mongoDb["fs.files"].find_one({"user_id": userId, "_id": picId})
  if not res:
    raise Exception("Image with id '%s' not found or not allowed" %id)
  else:
    mongoDb["fs.files"].delete_one({"image_id": picId})
    mongoDb["fs.files"].delete_one({"_id": picId})

#---------------------------------------------------
def check_carousel_owner(username:str, id:str):
  mongoDb = create_mongo_cli()
  userId = get_user_by_name(username=username, object_id=1)["_id"]

  qry = {
    "_id": ObjectId(id),
    "user_id": ObjectId(userId)
  }
  print(qry)

  res = mongoDb.carousels.find_one(qry)
  # print(res)
  return res

#--------------------------
def get_carousels(username:str, thumbs=False):

  userId = get_user_by_name(username=username, object_id=1)["_id"]

  mongoDb = create_mongo_cli()
  qry = [ 
    { '$addFields': {
      '_id': { '$toString': '$_id' },
      'user_id': { '$toString': '$user_id' },
    }}
  ]
  dbRes = mongoDb.carousels.aggregate(qry)
  return list(dbRes)

#--------------------------
def add_carousel(item:dict, username:str):
  userId = get_user_by_name(username=username, object_id=1)["_id"]
  item["user_id"] = userId
  mongoDb = create_mongo_cli()
  mongoDb.carousels.insert_one(item)
  res = dict(item)
  del res["_id"]
  del res["user_id"]
  return res

#--------------------------
def replace_carousel_by_id(username:str, id:str, item:dict):
  
  chk = check_carousel_owner(username=username, id=id)
  if not chk:
    raise Exception("Carousel with id '%s' not found or not allowed" %id)
  
  mongoDb = create_mongo_cli()
  qry = {"_id": ObjectId(id)}
  mongoDb.carousels.replace_one(qry, item)
  
  return item

#--------------------------
def delete_carousel_by_id(username:str, id:str):
  
  chk = check_carousel_owner(username=username, id=id)
  if not chk:
    raise Exception("Carousel with id '%s' not found or not allowed" %id)
  
  mongoDb = create_mongo_cli()
  res = mongoDb.carousels.delete_one({"_id": ObjectId(id)})
  
  return res

#--------------------------


#--------------------------


#--------------------------







#--------------------------------------------------------------------