import os
from fastapi import APIRouter, HTTPException, status


filter_router = APIRouter(prefix="/filter")

DATA_FOLDER = "data"


@filter_router.get("/gallery/{name}")
async def filter_gallery(name: str):
    if not os.path.exists(DATA_FOLDER):
        raise HTTPException(status_code=404, detail="Data folder not found.")

    for author_folder in os.listdir(DATA_FOLDER):
        author_path = os.path.join(DATA_FOLDER, author_folder)
        if os.path.isdir(author_path): 
            gallery_path = os.path.join(author_path, name)
            if os.path.exists(gallery_path) and os.path.isdir(gallery_path):
                return {"files": os.listdir(gallery_path)}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Gallery '{name}' not found.")
