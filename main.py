from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import app.Routers.Chatbot as Chatbot
from app.Models import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Chatbot.router, tags=["Chatbot"], prefix="/api/v1")

app.mount("/upload", StaticFiles(directory="./upload"), name="upload")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7007, reload=True)
