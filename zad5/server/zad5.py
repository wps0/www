from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

class Image(BaseModel):
    src: str
    title: str | None = None
    tags: list[str]

images_store = [
    Image(src="https://upload.wikimedia.org/wikipedia/commons/d/db/Tatra_mountains_western_side_2.jpg",
            title="Tatra mountains",
            tags=["tatra"]),
    Image(src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Okol%C3%AD_Hukliv%C3%A9ho_001.jpg/1280px-Okol%C3%AD_Hukliv%C3%A9ho_001.jpg",
            title="Beskids mountains",
            tags=["tatra"]),
    Image(src="https://worekraczanski.pl/wp-content/uploads/2023/03/wielka-racza-schronisko-pttk-na-wielkiej-raczy-1024x585x70.jpg",
            title="Wielka Racza PTTK Mountain Shelter",
            tags=["beskids", "shelter"]),
    Image(src="abc",
            title="unloadable",
            tags=[])
]

PAGE_SIZE = 5


app = FastAPI()
snapshot = 1

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/images")
async def get_images():
    global snapshot
    return {"snapshot": snapshot, "images": images_store}

@app.get("/images/total")
def get_images_total():
    global snapshot
    return {"snapshot": snapshot, "total_images": len(images_store)}

@app.get("/images/add/{count}")
def add_images(count: int):
    global snapshot
    global images_store
    for i in range(count):
        images_store.append(Image(src="abc", title="artificial image " + str(i), tags=['artificial']))
        snapshot += 1
