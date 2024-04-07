from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")


# Function to connect to MongoDB
def connect_to_mongodb():
    try:
        
        client = MongoClient(MONGO_CONNECTION_STRING)
        
        db = client.students
        
        print("Connected to MongoDB")
        print(MONGO_CONNECTION_STRING)
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
