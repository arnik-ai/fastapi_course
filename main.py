from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# --- Database Setup ---
client = MongoClient("mongodb://localhost:27017")
db = client["course_db"]

instructors_col = db["instructors"]
students_col = db["students"]
courses_col = db["courses"]
enrollments_col = db["enrollments"]

# --- Pydantic Schemas ---

# Instructor
class InstructorCreate(BaseModel):
    name: str
    email: EmailStr
    expertise: Optional[str] = None

class Instructor(InstructorCreate):
    id: Optional[str] = Field(alias="_id")
    class Config:
        populate_by_name = True

# Student
class StudentCreate(BaseModel):
    name: str
    email: EmailStr

class Student(StudentCreate):
    id: Optional[str] = Field(alias="_id")
    class Config:
        populate_by_name = True

# Course
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructor_id: str

class Course(CourseCreate):
    id: Optional[str] = Field(alias="_id")
    class Config:
        populate_by_name = True

# Enrollment
class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str
    timestamp: datetime = datetime.utcnow()

class Enrollment(EnrollmentCreate):
    id: Optional[str] = Field(alias="_id")
    class Config:
        populate_by_name = True


# --- FastAPI App ---
app = FastAPI(title="Course API")

# --- Instructor Router ---
instructor_router = APIRouter(prefix="/instructors", tags=["Instructors"])

@instructor_router.post("/", response_model=Instructor, status_code=status.HTTP_201_CREATED)
def create_instructor(instructor: InstructorCreate):
    res = instructors_col.insert_one(instructor.dict())
    return Instructor(id=str(res.inserted_id), **instructor.dict())

@instructor_router.get("/", response_model=List[Instructor])
def list_instructors():
    docs = list(instructors_col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@instructor_router.get("/{instructor_id}", response_model=Instructor)
def get_instructor(instructor_id: str):
    try:
        obj_id = ObjectId(instructor_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    doc = instructors_col.find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(404, "Instructor not found")
    doc["_id"] = str(doc["_id"])
    return doc

@instructor_router.put("/{instructor_id}", response_model=Instructor)
def update_instructor(instructor_id: str, data: InstructorCreate):
    try:
        obj_id = ObjectId(instructor_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    result = instructors_col.update_one({"_id": obj_id}, {"$set": data.dict()})
    if result.matched_count == 0:
        raise HTTPException(404, "Instructor not found")
    doc = instructors_col.find_one({"_id": obj_id})
    doc["_id"] = str(doc["_id"])
    return doc

@instructor_router.delete("/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor(instructor_id: str):
    try:
        obj_id = ObjectId(instructor_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    result = instructors_col.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Instructor not found")
    return


# --- Student Router ---
student_router = APIRouter(prefix="/students", tags=["Students"])

@student_router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    res = students_col.insert_one(student.dict())
    return Student(id=str(res.inserted_id), **student.dict())

@student_router.get("/", response_model=List[Student])
def list_students():
    docs = list(students_col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@student_router.get("/{student_id}", response_model=Student)
def get_student(student_id: str):
    try:
        obj_id = ObjectId(student_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    doc = students_col.find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(404, "Student not found")
    doc["_id"] = str(doc["_id"])
    return doc

@student_router.put("/{student_id}", response_model=Student)
def update_student(student_id: str, data: StudentCreate):
    try:
        obj_id = ObjectId(student_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    result = students_col.update_one({"_id": obj_id}, {"$set": data.dict()})
    if result.matched_count == 0:
        raise HTTPException(404, "Student not found")
    doc = students_col.find_one({"_id": obj_id})
    doc["_id"] = str(doc["_id"])
    return doc

@student_router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str):
    try:
        obj_id = ObjectId(student_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    result = students_col.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Student not found")
    return


# --- Course Router ---
course_router = APIRouter(prefix="/courses", tags=["Courses"])

@course_router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    res = courses_col.insert_one(course.dict())
    return Course(id=str(res.inserted_id), **course.dict())

@course_router.get("/", response_model=List[Course])
def list_courses():
    docs = list(courses_col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@course_router.get("/{course_id}", response_model=Course)
def get_course(course_id: str):
    try:
        obj_id = ObjectId(course_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    doc = courses_col.find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(404, "Course not found")
    doc["_id"] = str(doc["_id"])
    return doc

@course_router.put("/{course_id}", response_model=Course)
def update_course(course_id: str, data: CourseCreate):
    try:
        obj_id = ObjectId(course_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    result = courses_col.update_one({"_id": obj_id}, {"$set": data.dict()})
    if result.matched_count == 0:
        raise HTTPException(404, "Course not found")
    doc = courses_col.find_one({"_id": obj_id})
    doc["_id"] = str(doc["_id"])
    return doc

@course_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: str):
    try:
        obj_id = ObjectId(course_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    result = courses_col.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Course not found")
    return

@course_router.get("/instructor/{instructor_id}", response_model=List[Course])
def get_courses_by_instructor(instructor_id: str):
    docs = list(courses_col.find({"instructor_id": instructor_id}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


# --- Enrollment Router ---
enrollment_router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@enrollment_router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment: EnrollmentCreate):
    res = enrollments_col.insert_one(enrollment.dict())
    return Enrollment(id=str(res.inserted_id), **enrollment.dict())

@enrollment_router.get("/", response_model=List[Enrollment])
def list_enrollments():
    docs = list(enrollments_col.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@enrollment_router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: str):
    try:
        obj_id = ObjectId(enrollment_id)
    except Exception:
        raise HTTPException(400, "Invalid id format")
    result = enrollments_col.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Enrollment not found")
    return

@enrollment_router.get("/student/{student_id}/courses", response_model=List[Course])
def get_courses_of_student(student_id: str):
    enrolls = list(enrollments_col.find({"student_id": student_id}))
    course_ids = [e["course_id"] for e in enrolls]
    docs = list(courses_col.find({"_id": {"$in": [ObjectId(cid) for cid in course_ids]}}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs

@enrollment_router.get("/course/{course_id}/students", response_model=List[Student])
def get_students_of_course(course_id: str):
    enrolls = list(enrollments_col.find({"course_id": course_id}))
    student_ids = [e["student_id"] for e in enrolls]
    docs = list(students_col.find({"_id": {"$in": [ObjectId(sid) for sid in student_ids]}}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


# --- Include Routers ---
app.include_router(instructor_router)
app.include_router(student_router)
app.include_router(course_router)
app.include_router(enrollment_router)

