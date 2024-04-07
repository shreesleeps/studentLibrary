from fastapi import HTTPException, Query
from models.student_model import Student
from config.db import connect_to_mongodb
from bson.objectid import ObjectId


# Connect to MongoDB
db = connect_to_mongodb()

# Create Students
async def create_student(student: Student):
    response = db.students.insert_one(student.model_dump())
    return {"id": str(response.inserted_id)}

# List students
async def list_students(country: str = Query(None, description="Country to filter by"), age: int = Query(None, description="Minimum age to filter by")):
    filter_query = {}
    
    # Apply country filter if provided
    if country:
        filter_query["address.country"] = country
    
    # Apply age filter if provided
    if age is not None:
        filter_query["age"] = {"$gte": age}
    
    # Fetch students from the database based on the filter query
    response = db.students.find(filter_query)
    
    # Convert the cursor to a list of dictionaries
    student_list = []
    for student in response:
        student_data = {
            "name": student["name"],
            "age": student["age"]
        }
        student_list.append(student_data)
    
    return {"data": student_list}

# Fetch student
async def get_student(id: str):
    response = db.students.find_one({"_id": ObjectId(id)})
    if response is not None:
        address = response.get("address", {})
        response = {
            "name": response["name"],
            "age": response["age"],
            "address": {
                "city": address.get("city", ""),
                "country": address.get("country", "")
            }
        }
        return response
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# Update student
async def update_student(id: str, student: Student):
    result = db.students.update_one({"_id": ObjectId(id)}, {"$set": student.model_dump()})
    if result.modified_count == 1:
        return {}
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# Delete student
async def delete_student(id: str):
    result = db.students.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
