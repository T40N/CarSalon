import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://salon:salon@localhost:5432/salon_vehicle')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
