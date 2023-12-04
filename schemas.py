from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
import models
from uuid import UUID

T = TypeVar('T')

class StudentSchema(BaseModel):
    student_id: Optional[int] = None  # Mengganti "user_id" menjadi "student_id"
    username: Optional[str] = None
    fullname: Optional[str] = None
    email: Optional[str] = None
    interest: Optional[str] = None

    class Config:
        orm_mode = True

class ClassSchema(BaseModel):
    class_id: Optional[int] = None
    class_name: Optional[str] = None
    class_description: Optional[str] = None
    class_instructor: Optional[int] = None

    class Config:
        orm_mode = True

class InstructorSchema(BaseModel):
    instructor_id: Optional[int] = None
    instructor_name: Optional[str] = None
    instructor_bio: Optional[str] = None
    instructor_specialty: Optional[str] = None

    class Config:
        orm_mode = True

class StudentInterestSchema(BaseModel):
    id: Optional[int] = None
    student_id: Optional[int] = None  # Mengganti "user_id" menjadi "student_id"
    interest: Optional[str] = None

    class Config:
        orm_mode = True

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class RequestStudent(BaseModel):
    parameter: StudentSchema = Field(...)

class RequestClass(BaseModel):
    parameter: ClassSchema = Field(...)

class RequestInstructor(BaseModel):
    parameter: InstructorSchema = Field(...)

class RequestStudentInterest(BaseModel):
    parameter: StudentInterestSchema = Field(...)

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

def student_model_to_schema(student: models.Student) -> StudentSchema:
    return StudentSchema(
        student_id=student.student_id,  # Mengganti "user_id" menjadi "student_id"
        username=student.username,
        fullname=student.fullname,
        email=student.email,
        interest=student.interest
    )

def class_model_to_schema(class_: models.Class) -> ClassSchema:
    return ClassSchema(
        class_id=class_.class_id,
        class_name=class_.class_name,
        class_description=class_.class_description,
        class_instructor=class_.class_instructor
    )

def instructor_model_to_schema(instructor: models.Instructor) -> InstructorSchema:
    return InstructorSchema(
        instructor_id=instructor.instructor_id,
        instructor_name=instructor.instructor_name,
        instructor_bio=instructor.instructor_bio,
        instructor_specialty=instructor.instructor_specialty
    )

def student_interest_model_to_schema(student_interest: models.StudentInterest) -> StudentInterestSchema:
    return StudentInterestSchema(
        id=student_interest.id,
        student_id=student_interest.student_id,  # Mengganti "user_id" menjadi "student_id"
        interest=student_interest.interest
    )