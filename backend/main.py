import glob
import io
import os

import aiofiles
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from image_processing import process_image
from database_service import image_repository

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


@app.post("/file")
async def create_file(file: UploadFile = File(...)):
    async with aiofiles.open(f'D:/Faculta/anul3/Licenta/backend/resources/images/{file.filename}', 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        image = Image.open(io.BytesIO(content)).convert('RGB')
        bytes_image = io.BytesIO()
        image.save(bytes_image, format='jpeg')

        all_symbols = process_image.get_notes(f'resources/images/{file.filename}')

        image_repository.insert_processed_image(file.filename, all_symbols)

    return all_symbols


@app.get("/image/{filename}")
async def get_file(filename: str):
    im = Image.open(f'D:/Faculta/anul3/Licenta/backend/resources/images/{filename}')
    im_resize = im.resize((300, 300))
    buf = io.BytesIO()
    im_resize.save(buf, format='jpeg')

    return Response(content=buf.getvalue(), status_code=200, media_type="image/jpg")


@app.get("/filepaths")
async def get_filePaths():
    image_paths = []
    for filename in glob.glob('D:/Faculta/anul3/Licenta/backend/resources/images/*'):
        image_paths.append(os.path.basename(filename))
    return image_paths


@app.get("/processed_image/{filename}")
async def get_processed_image(filename):
    return image_repository.read_processed_image(filename)