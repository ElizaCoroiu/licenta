from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from image_processing import process_image

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

all_symbols = process_image.get_notes('resources/images/mary.jpg')

@app.get("/notes")
async def get():
    return all_symbols

@app.post("/file")
async def create_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
