import crud
from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import StudentSchema, ClassSchema, InstructorSchema, StudentInterestSchema, Request, Response, RequestStudent, RequestClass, RequestInstructor, RequestStudentInterest, student_model_to_schema, class_model_to_schema, instructor_model_to_schema, student_interest_model_to_schema
from typing import Annotated
from models import User
import requests

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
import json
from fastapi.encoders import jsonable_encoder

students = APIRouter()
instructors = APIRouter()
classes = APIRouter()
studentinterest = APIRouter()
recommendations = APIRouter()
authentication = APIRouter()
json_filename="user.json"

integratedToken = ''

with open(json_filename, "r") as read_file:
    data = json.load(read_file)

def write_data(data):
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
JWT_SECRET = 'myjwtsecret'
ALGORITHM = 'HS256'

def get_user_by_username(username):
    for desain_user in data['user']:
        if desain_user['username'] == username:
            return desain_user
    return None

def authenticate_user(username: str, password: str):
    user_data = get_user_by_username(username)
    if not user_data:
        return None

    user = User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'])

    if not user.verify_password(password):
        return None

    return user

@authentication.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    global integratedToken
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        print(f"Invalid username or password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    url = 'https://bevbuddy.up.railway.app/login'
    data = {
        'username': form_data.username,
        'password': form_data.password
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            global integratedToken
            integratedToken = result.get('token')
            token = jwt.encode({'id': user.id, 'username': user.username}, JWT_SECRET, algorithm=ALGORITHM)
        except ValueError as e:
            print("Invalid JSON format in response:", response.text)
            return {'Error': 'Invalid JSON format in response'}
        return {'access_token': token, 'token_type': 'bearer', 'integrasiToken' : integratedToken}
    else:
        return {'Error': response.status_code, 'Detail': response.text}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = get_user_by_username(payload.get('username'))
        return User(id=user['id'], username=user['username'], password_hash=user['password_hash'])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

@authentication.post('/user')
async def create_user(user_info: dict):
    username = user_info.get('username')
    fullname = user_info.get('fullname')
    password = user_info.get('password')
    email = user_info.get('email')

    if not username or not password or not fullname or not email:
        raise HTTPException(status_code=422, detail='All fields are required')

    for existing_user in data['user']:
        if existing_user['username'] == username:
            return {"error": "Username already taken"}

    last_user_id = data['user'][-1]['id'] if data['user'] else 0
    user_id = last_user_id + 1
    user = jsonable_encoder(User(id=user_id, username=username, password_hash=bcrypt.hash(password)))
    data['user'].append(user)

    url = 'https://bevbuddy.up.railway.app/register'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    user_data = {
        "username": username,
        "fullname": fullname,
        "email": email + "@gmail.com",
        "password": password,
        "role": "customer",
        "token": "tokenmichael"
    }

    try:
        response = requests.post(url, headers=headers, json=user_data)
        response.raise_for_status()
        return {"username": username, "password": password, "email": email + "@gmail.com", "integratedRegister": response.json()}
    except requests.exceptions.RequestException as err:
        print(f"Error during request: {err}")
        return {"error": "An unexpected error occurred"}
    finally:
        write_data(data)

@authentication.get('/users/me')
async def get_user(user: User = Depends(get_current_user)):
    return {'id': user.id, 'username': user.username, 'role': 'admin'}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@students.post('/users')
async def create_user(username: str, fullname: str, password: str, email: str):
    for existing_user in data['user']:
        if existing_user['username'] == username:
            # Username already exists, return an appropriate response
            return {"error": "Username already taken"}

    last_user_id = data['user'][-1]['id'] if data['user'] else 0
    user_id = last_user_id + 1
    user = jsonable_encoder(User(id=user_id, username=username, password_hash=bcrypt.hash(password)))
    data['user'].append(user)

    url = 'https://bevbuddy.up.railway.app/register'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    user_data = {
        "username": username,
        "fullname": fullname,
        "email": email + "@gmail.com",
        "password": password,
        "role": "customer",
        "token": "tokenmichael"
    }

    try:
        response = requests.post(url, headers=headers, json=user_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return {"username": username, "password": password, "email": email + "@gmail.com", "integratedRegister": response.json()}
    except requests.exceptions.RequestException as err:
        print(f"Error during request: {err}")
        return {"error": "An unexpected error occurred"}
    finally:
        write_data(data)

@students.get("/students/")
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    students = crud.get_students(db, skip, limit)
    student_schemas = [student_model_to_schema(student) for student in students]
    return Response(status="Ok", code="200", message="Success fetch all students", result=student_schemas)

@classes.get("/classes/")
async def get_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    classes = crud.get_classes(db, skip, limit)
    class_schemas = [class_model_to_schema(class_) for class_ in classes]
    return Response(status="Ok", code="200", message="Success fetch all classes", result=class_schemas)

@instructors.get("/instructors/")
async def get_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    instructors = crud.get_instructors(db, skip, limit)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in instructors]
    return Response(status="Ok", code="200", message="Success fetch all instructors", result=instructor_schemas)

@classes.get("/classes/{class_id}")
async def get_class_info_service(class_id: int = Path(..., title="Class ID", description="The class's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    class_info = crud.get_class_info(db, class_id)
    if class_info:
        class_schema = class_model_to_schema(class_info)
        return Response(status="Ok", code="200", message="Class information", result=class_schema)
    else:
        raise HTTPException(status_code=404, detail="Class not found")

@instructors.get("/instructors/{instructor_id}")
async def get_instructor_info_service(instructor_id: int = Path(..., title="Instructor ID", description="The instructor's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    instructor_info = crud.get_instructor_info(db, instructor_id)
    if instructor_info:
        instructor_schema = instructor_model_to_schema(instructor_info)
        return Response(status="Ok", code="200", message="Instructor information", result=instructor_schema)
    else:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
