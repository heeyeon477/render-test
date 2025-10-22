# check_users.py
from pymongo import MongoClient

client = MongoClient("mongodb+srv://<db_user>:<db_password>@cluster0.xuoij3g.mongodb.net")
db = client['carBackend']
users = db['users']

for user in users.find():
    print(f"Username: {user.get('username')}, User ID: {user.get('_id')}")
