import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost:5432/deepfake_demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "uploads"
