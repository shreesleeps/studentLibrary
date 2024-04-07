from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")


# Function to connect to MongoDB
def connect_to_mongodb():
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(MONGO_CONNECTION_STRING)
        # Access a specific database (replace "your_database" with the actual database name)
        db = client.students
        # Return the database object
        print("Connected to MongoDB")
        print(MONGO_CONNECTION_STRING)
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
