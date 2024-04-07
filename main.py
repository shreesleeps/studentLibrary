import uvicorn
from fastapi import FastAPI
from models.student_model import Student
from config.db import connect_to_mongodb
from routers.student_routers import router as student_router

app = FastAPI()


app.include_router(student_router, prefix="/api")




@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)