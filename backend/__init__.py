from fastapi import FastAPI


app = FastAPI()

from .routes import image_router, filter_router

app.include_router(image_router)
app.include_router(filter_router)