from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

class BaseConfig(BaseSettings):
    DB_URL: Optional[str]
    DB_NAME: Optional[str]
    CLOUDINARY_SECRET_KEY: Optional[str]
    CLOUDINARY_API_KEY: Optional[str]
    CLOUDINARY_CLOUD_NAME: Optional[str]
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Base = declarative_base()

class CarModel(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    manufacturer = Column(String)
