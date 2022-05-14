from fastapi import FastAPI
from image_processing import process_image

app = FastAPI()

all_symbols = process_image.get_notes('resources/images/mary.jpg')

@app.get("/api/GetNotes")
async def get():
    return all_symbols

