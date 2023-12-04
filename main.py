from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import models
from routes import authentication, students, classes, studentinterest, recommendations, instructors
from config import engine, SessionLocal
from sqlalchemy.orm import Session

# Membuat tabel dalam database (jika belum ada)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[""],
)

# Menambahkan rute yang telah Anda definisikan
app.include_router(authentication, tags=["Authtentication"])
app.include_router(recommendations, tags=["Recommendation"])
app.include_router(students, tags=["Student"])
app.include_router(classes, tags=["Class"])
app.include_router(instructors, tags=["Instructor"])