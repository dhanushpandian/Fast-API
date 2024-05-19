from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app=FastAPI()

'''
Get = get info
Post = create new info
Put = update info
Delete = delete info
'''

students = {
    1: {
        'name': 'Dhanush',
        'age': 21,
        'year': '3rd'
    },
    2: {
        'name': 'Raj',
        'age': 22,
        'year': '3rd'
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get('/')
def index():
    return {"data":"App Started"}

@app.get("/get-data/{student_id}")
def get_student(student_id:int = Path(...,description="The ID of the student you want to view")):
    return students[student_id]

@app.get("/get-by-name")
def get_student(*,name: Optional[str] = None):
    for student_id in students:
        if students['name']==name:
            return students[student_id]
    return {"data":"Not Found"}

@app.post("/add-data/{student_id}")
def add_data( student: Student,student_id :int ):
    if student_id in students:
        return {"Error":"Student already exists"}
    students[student_id] = student
    print(students)
    return students[student_id]

@app.put("/update-data/{student_id}")
def update_data(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    # Update student attributes if provided
    if student.name is not None:
        students[student_id]['name'] = student.name
    if student.age is not None:
        students[student_id]['age'] = student.age
    if student.year is not None:
        students[student_id]['year'] = student.year

    return students[student_id]

@app.delete("/delete-data/{student_id}")
def delete_data(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}