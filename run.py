from uvicorn import run as start

from backend import app


if __name__ == "__main__" :
    start("run:app")
