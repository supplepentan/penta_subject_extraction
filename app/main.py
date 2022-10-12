import os
import shutil
from io import BytesIO

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.params import File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from lib import make_mask, subject_extraction

UPLOAD_FOLDER = "./upload"
OUTPUT_FOLDER = "./output"
INPUT_IMAGE = os.path.join(UPLOAD_FOLDER, "input.png")
MASK_IMAGE = os.path.join(OUTPUT_FOLDER, "mask.png")
SUBJECT_EXTRACTION_IMAGE = os.path.join(OUTPUT_FOLDER, "subject_extraction.png")
CKPT_PATH = "./pretrained/modnet_photographic_portrait_matting.ckpt"


app = FastAPI(title="さぷりぺんたんの被写体検出", description="被写体を抽出するよ", version="1.0")

import mimetypes

mimetypes.init()
mimetypes.add_type("application/javascript", ".js")

#: Configure CORS
origins = ["http://localhost:8080", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./template/static"), name="static")
templates = Jinja2Templates(directory="./template/")


@app.get("/")
def index(request: Request):
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER)
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def index(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    image.save(INPUT_IMAGE)
    make_mask(CKPT_PATH, INPUT_IMAGE, MASK_IMAGE)
    subject_extraction(INPUT_IMAGE, MASK_IMAGE, SUBJECT_EXTRACTION_IMAGE)
    response = FileResponse(
        path=SUBJECT_EXTRACTION_IMAGE, filename="subject_extraction.png"
    )
    return response


if __name__ == "__main__":
    uvicorn.main(app=app)
