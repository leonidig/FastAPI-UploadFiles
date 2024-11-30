import asyncio
import os
from typing import List

from fastapi import APIRouter, status, UploadFile, Form, HTTPException, BackgroundTasks
from PIL import Image

from ..schemas import ResizeImage


image_router = APIRouter(prefix = "/image", tags = ["images"])

ALLOWED_MIME_TYPES = [
    "image/jpeg",  
    "image/png", 
    # "image/webp",  
    # "image/vnd.microsoft.icon",  
    # "image/svg+xml"  
]

DATA_FOLDER = "data"
try:
    os.mkdir(DATA_FOLDER)
except FileExistsError as e:
    print(e)


async def save_image(image_path: str, image: bytes):
    await asyncio.sleep(3)
    with open(image_path, "wb") as buffer:
        buffer.write(image)


@image_router.get("/")
async def read_root():
    return {"message" : "test root"}


@image_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(background_tasks: BackgroundTasks,
                       images: List[UploadFile] = [],
                       author: str = Form(...),
                       gallery: str = Form(...)):
    
    user_folder = f"{DATA_FOLDER}/{author}"
    gallery_folder = f"{user_folder}/{gallery}"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    if not os.path.exists(gallery_folder):
        os.mkdir(gallery_folder)
    for image in images:
        if image.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                detail=f"Unsupported content type ({image.content_type}) for image {image.filename}, allowed - {', '.join(ALLOWED_MIME_TYPES)}",
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        image_path = f"{gallery_folder}/{image.filename}"
        background_tasks.add_task(save_image, image_path=image_path, image=await image.read())
    
    return {"message": "Images are being uploaded in the background."}


async def resize_image(data: ResizeImage):
    folder = f"{DATA_FOLDER}/{data.author}/{data.gallery}"
    image_path = os.path.join(folder, data.image)
    
    if not os.path.exists(image_path):
        raise HTTPException(
            detail=f"Image {data.image} not found at {folder}",
            status_code=status.HTTP_404_NOT_FOUND
        )
    try:
        with Image.open(image_path) as image:
            resized_image = image.resize((data.width, data.height))
            resize_image_path = os.path.join(folder, f"resized_{data.image}")
            resized_image.save(resize_image_path)
            return {"message": f"Image resized successfully", "resized_image_path": resize_image_path}
    except Exception as e:
        raise HTTPException(
            detail = e,
            status_code = status.HTTP_400_BAD_REQUEST
        )
    



@image_router.post("/resize", status_code = status.HTTP_202_ACCEPTED)
async def resize(data: ResizeImage,
                 background_tasks: BackgroundTasks):
    background_tasks.add_task(resize_image, data)
    return "Ok"
    