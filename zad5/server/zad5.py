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
snapshot = 0

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

def paginate(images: list[Image], page: int) -> list[Image]:
    pages = (len(images) + PAGE_SIZE - 1) // PAGE_SIZE
    imgs_len = len(images)
    offset = PAGE_SIZE * (page - 1)
    imgs = []

    if page <= 0 or offset > imgs_len:
        page_len = 0
    elif page < pages:
        page_len = PAGE_SIZE
        imgs = images[offset:offset + page_len]
    else:
        page_len = imgs_len - (page-1) * PAGE_SIZE
        imgs = images[offset:offset + page_len]

    return {
        "snapshot": snapshot,
        "total_images": len(images),
        "pages": pages,
        "count": page_len,
        "images": imgs
    }

def any_starts_with(strings: list[str], prefix: str) -> bool:
    for s in strings:
        if s.startswith(prefix):
            return True
    return False

@app.get("/images/p/{page}")
async def get_images(page: int):
    return paginate(images_store, page)

@app.get("/images/total")
def get_images_total():
    return {"snapshot": snapshot, total_images": len(images_store), "pages": (len(images_store) + 1) // PAGE_SIZE}

@app.get("/images/add/{count}")
def add_images(count: int):
    global images_store
    for i in range(count):
        images_store.append(Image(src="abc", title="artificial image " + str(i), tags=['artificial']))
        snapshot += 1


@app.get("/images/p/{page}/{tag}")
async def get_images(page: int, tag: str):
    tagged_images = [x for x in images_store if any_starts_with(x.tags, tag)]
    return paginate(tagged_images, page)