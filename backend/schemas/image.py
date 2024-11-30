from pydantic import BaseModel


class ResizeImage(BaseModel):
    author: str
    gallery: str
    image: str
    height: int
    width: int