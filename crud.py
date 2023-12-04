from sqlalchemy.orm import Session
from models import Student, Class, Instructor, StudentInterest
from schemas import (
    StudentSchema, ClassSchema, InstructorSchema, StudentInterestSchema
)

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.student_id == student_id).first()

def create_student(db: Session, student: StudentSchema):
    _student = Student(
        username=student.username,
        fullname=student.fullname,
        email=student.email,
        interest=student.interest
    )
    db.add(_student)
    db.commit()
    db.refresh(_student)
    return _student

def remove_student(db: Session, student_id: int):
    _student = get_student_by_id(db=db, student_id=student_id)
    db.delete(_student)
    db.commit()

def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Class).offset(skip).limit(limit).all()

def get_class_by_id(db: Session, class_id: int):
    return db.query(Class).filter(Class.class_id == class_id).first()

def create_class(db: Session, class_: ClassSchema):
    _class = Class(
        class_name=class_.class_name,
        class_description=class_.class_description,
        class_instructor=class_.class_instructor
    )
    db.add(_class)
    db.commit()
    db.refresh(_class)
    return _class

def remove_class(db: Session, class_id: int):
    _class = get_class_by_id(db=db, class_id=class_id)
    db.delete(_class)
    db.commit()

def get_instructors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Instructor).offset(skip).limit(limit).all()

def get_instructor_by_id(db: Session, instructor_id: int):
    return db.query(Instructor).filter(Instructor.instructor_id == instructor_id).first()

def create_instructor(db: Session, instructor: InstructorSchema):
    _instructor = Instructor(
        instructor_name=instructor.instructor_name,
        instructor_bio=instructor.instructor_bio,
        instructor_specialty=instructor.instructor_specialty
    )
    db.add(_instructor)
    db.commit()
    db.refresh(_instructor)
    return _instructor

def remove_instructor(db: Session, instructor_id: int):
    _instructor = get_instructor_by_id(db=db, instructor_id=instructor_id)
    db.delete(_instructor)
    db.commit()

def get_student_interests(db: Session, student_id: int):
    return db.query(StudentInterest.interest).filter(StudentInterest.student_id == student_id).all()

def add_student_interest(db: Session, student_id: int, interest: str):
    student_interest = StudentInterest(student_id=student_id, interest=interest)
    db.add(student_interest)
    db.commit()
    db.refresh(student_interest)

def remove_student_interest(db: Session, student_id: int, interest: str):
    db.query(StudentInterest).filter(StudentInterest.student_id == student_id, StudentInterest.interest == interest).delete()
    db.commit()

# Fungsi untuk mendapatkan rekomendasi kelas berdasarkan minat
def get_class_recommendations(db: Session, student_id: int):
    # Mengambil minat mahasiswa
    student_interests = db.query(StudentInterest.interest).filter(StudentInterest.student_id == student_id).all()
    student_interests = [interest[0] for interest in student_interests]

    # Mengambil kelas yang sesuai dengan minat mahasiswa
    recommended_classes = db.query(Class).join(Instructor, Instructor.instructor_id == Class.class_instructor).filter(
        Instructor.instructor_specialty.in_(student_interests)
    ).all()

    return recommended_classes

# Fungsi untuk mendapatkan rekomendasi instruktur berdasarkan minat
def get_instructor_recommendations(db: Session, student_id: int):
    # Mengambil minat mahasiswa
    student_interests = db.query(StudentInterest.interest).filter(StudentInterest.student_id == student_id).all()
    student_interests = [interest[0] for interest in student_interests]

    # Mengambil instruktur yang sesuai dengan minat mahasiswa
    recommended_instructors = db.query(Instructor).filter(Instructor.instructor_specialty.in_(student_interests)).all()

    return recommended_instructors

# Fungsi untuk mendapatkan kelas yang diambil oleh seorang mahasiswa
def get_classes_taken_by_student(db: Session, student_id: int):
    return db.query(Class).join(Student, Class.class_id == Student.student_id).filter(
        Student.student_id == student_id
    ).all()

# Fungsi untuk mendapatkan instruktur yang diajar oleh seorang mahasiswa
def get_instructors_taught_by_student(db: Session, student_id: int):
    return db.query(Instructor).join(Class, Class.class_instructor == Instructor.instructor_id).join(
        Student, Class.class_id == Student.student_id
    ).filter(Student.student_id == student_id).all()

# Fungsi untuk mendapatkan informasi tentang sebuah kelas berdasarkan ID
def get_class_info(db: Session, class_id: int):
    return db.query(Class).filter(Class.class_id == class_id).first()

# Fungsi untuk mendapatkan informasi tentang seorang instruktur berdasarkan ID
def get_instructor_info(db: Session, instructor_id: int):
    return db.query(Instructor).filter(Instructor.instructor_id == instructor_id).first()

def update_student_interest(db: Session, student_id: int, old_interest: str, new_interest: str):
    db.query(StudentInterest).filter(StudentInterest.student_id == student_id, StudentInterest.interest == old_interest).update({"interest": new_interest})
    db.commit()

# Modify the existing update functions

def update_student(db: Session, student_id: int, updated_data: dict):
    db.query(Student).filter(Student.student_id == student_id).update(updated_data)
    db.commit()

def update_class(db: Session, class_id: int, updated_data: dict):
    db.query(Class).filter(Class.class_id == class_id).update(updated_data)
    db.commit()

def update_instructor(db: Session, instructor_id: int, updated_data: dict):
    db.query(Instructor).filter(Instructor.instructor_id == instructor_id).update(updated_data)
    db.commit()
