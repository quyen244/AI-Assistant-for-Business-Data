from fastapi import FastAPI, Path 
from pydantic import BaseModel
import logging 

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = FastAPI()
students = {
    1: {"name": "Alice", "age": 20},
    2: {"name": "Bob", "age": 22}
}
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
# path parameter example
@app.get("/students/{student_id}")
def read_student(student_id: int = Path(..., description="The ID of the student to retrieve")):
    return students.get(student_id)

# query parameter example
@app.get("/students/")
def get_student_by_name(name : str = None):
    for student_id, student in students.items():
        if student['name'] == name:
            return student
    return {"message" : "Student not found"}

class Student(BaseModel):
    name: str
    age: int


@app.post("/students/")
def create_student(student : Student):
    student_id = max(students.keys()) + 1
    
    students[student_id] = student

    return {"id" : student_id , "name" : student.name , "age" : student.age}
# uvicorn main:app --reload