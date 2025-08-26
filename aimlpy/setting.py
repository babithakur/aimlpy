"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)


class Settings(object):
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    API_PORT = int(os.getenv('API_PORT', 8000))

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_NAME = os.getenv('DB_NAME', 'aimlpy')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Passw0rd')
    DATABASE_URL = os.getenv('DB_URL', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
