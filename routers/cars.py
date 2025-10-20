from bson import ObjectId
from typing import Optional
from fastapi import (
    APIRouter, 
    Body, 
    File,
    Form,
    HTTPException, 
    Request,
    UploadFile, 
    status,
)
from fastapi.responses import Response
from pymongo import ReturnDocument
import cloudinary
from cloudinary import uploader # noqa: F401
from config import BaseConfig
from models import CarModel, CarCollection

settings = BaseConfig()
router = APIRouter()
CARS_PER_PAGE = 10

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_SECRET_KEY,
)

@router.post (
    "/",
    response_description="Add new car with picture",
    response_model=CarModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)

async def add_car_with_picture(
    request: Request,
    brand: str = Form(...),
    make: str = Form(...),
    year: int = Form(...),
    cm3: int = Form(...),
    km: int = Form(...),
    price: int = Form(...),
    # Accept either a picture URL (string) or an uploaded file. The client
    # can send `picture_url` as a plain form field (string) or an actual file
    # under `picture_file` (multipart). We prefer the uploaded file when both
    # are provided.
    picture_url: Optional[str] = Form(None),
    picture_file: Optional[UploadFile] = File(None),
):

    picture_url_result: Optional[str] = None

    if picture_file is not None:
        # upload provided file
        cloudinary_image = cloudinary.uploader.upload(
            picture_file.file, crop="fill", width=800
        )
        picture_url_result = cloudinary_image.get("secure_url")
    elif picture_url:
        # use the provided URL as-is
        picture_url_result = picture_url

    car = CarModel (
        brand=brand, # type: ignore
        make=make, # type: ignore
        year=year, # type: ignore
        cm3=cm3, # type: ignore
        km=km, # type: ignore
        price=price, # type: ignore
        picture_url=picture_url_result
    )
    cars = request.app.db["cars"]
    document = car.model_dump(by_alias=True, exclude=["id"]) 
    inserted = await cars.insert_one(document)

    doc = await cars.find_one({"_id": inserted.inserted_id})
    # convert ObjectId to str so Pydantic can validate/serialize it
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


"""
async def add_car(request: Request, car: CarModel = Body(...)):
    cars = request.app.db["cars"]
    document = car.model_dump (
        by_alias=True, exclude=['id'])
    inserted = await cars.insert_one(document)
    return await cars.find_one({"_id": inserted.inserted_id})
"""

@router.get(
    "/",
    response_description="List all cars",
    response_model=CarCollection,
    response_model_by_alias=False,
)

async def list_cars(request: Request):
    cars = request.app.db["cars"]
    results = []
    cursor = cars.find()
    async for document in cursor:
        results.append(document)
    return CarCollection(cars=await cars.find().to_list(1000))

@router.get(
    "/{id}",
    response_description="Get a single car by ID",
    response_model=CarModel,
    response_model_by_alias=False,
)

async def show_car(id: str, request: Request):
    cars = request.app.db["cars"]
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Car {id} not found")
    if (car := await cars.find_one({"_id": ObjectId(id)})) is not None:
        return car
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")