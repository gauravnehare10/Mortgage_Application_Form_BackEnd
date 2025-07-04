from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import find_dotenv, load_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

MONGO_URL = os.getenv("MONGO_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

db_client = AsyncIOMotorClient(MONGO_URL)

db = db_client.MortgageData

users_collection = db.user_details

applicants = db.applicants
mortgage_form = db.mortgage_form
