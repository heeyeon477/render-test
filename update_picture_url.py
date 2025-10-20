from pymongo import MongoClient
from bson import ObjectId

# MongoDB 연결
client = MongoClient("mongodb+srv://gimh64627_db_user:IwhbeRohjcpjfrlY@cluster0.xuoij3g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.carBackend
cars = db.cars

# 기존 모든 car에 picture_url 넣기
# 예시 URL
default_url = "https://res.cloudinary.com/duro3h5of/image/upload/v1758254271/ux2wrhstfbk91ehikmvj.jpg"

for car in cars.find({"picture_url": None}):
    cars.update_one(
        {"_id": car["_id"]},
        {"$set": {"picture_url": default_url}}
    )
    print(f"Updated car {"_id"} with default picture_url")
