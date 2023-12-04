from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Base, SessionLocal

class Student(Base):
    __tablename__ = "student"

    student_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    fullname = Column(String)
    email = Column(String)
    interest = Column(String)

    # Menyambungkan Student dengan minat mereka
    interests = relationship("StudentInterest", back_populates="student")

class Class(Base):
    __tablename__ = "class"

    class_id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String)
    class_description = Column(String)
    class_instructor = Column(Integer, ForeignKey('instructor.instructor_id'))

    # Menyambungkan Class dengan Instructor
    instructor = relationship("Instructor", back_populates="classes")

class Instructor(Base):
    __tablename__ = "instructor"

    instructor_id = Column(Integer, primary_key=True, index=True)
    instructor_name = Column(String)
    instructor_bio = Column(String)
    instructor_specialty = Column(String)

    # Menyambungkan Instructor dengan kelas yang dia ajar
    classes = relationship("Class", back_populates="instructor")

class StudentInterest(Base):
    __tablename__ = "student_interest" 

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))  
    interest = Column(String)

    # Menyambungkan StudentInterest dengan Student
    student = relationship("Student", back_populates="interests")  

# Fungsi untuk mengambil rekomendasi
def get_recommendations(student_id):
    session = SessionLocal()
    try:
        # Mendapatkan minat pengguna
        student_interests = session.query(StudentInterest.interest).filter(StudentInterest.student_id == student_id).all()  # Mengganti "UserInterest" menjadi "StudentInterest"
        student_interests = [interest[0] for interest in student_interests]

        # Mencari kelas yang sesuai dengan minat pengguna
        recommended_classes = session.query(Class).join(Instructor, Instructor.instructor_id == Class.class_instructor).filter(Class.class_instructor != student_id, Instructor.instructor_specialty.in_(student_interests)).all()

        return recommended_classes
    finally:
        session.close()

from passlib.hash import bcrypt
class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)