from fastapi import HTTPException
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
async def list_students():
    response = db.students.find({})
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
