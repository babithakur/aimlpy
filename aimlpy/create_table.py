from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from aimlpy.repo.datasource import Base
from aimlpy.model.user_notes import UserNotes  


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
