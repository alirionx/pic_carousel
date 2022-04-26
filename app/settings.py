import os

env_data_map = {
  "jwt_secret": "VERYSECRET",
  "jwt_algo": "HS256",
  "mongodb_host": "localhost",
  "mongodb_port": 27017,
  "mongodb_user": "ANON",
  "mongodb_secret": "VERYSECRET"
}


for key,val in env_data_map.items():
  if os.environ.get(key):
    env_data_map[key] = val

