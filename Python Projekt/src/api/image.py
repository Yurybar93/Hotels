from fastapi import APIRouter, UploadFile

import shutil

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("")
def uploade_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(f"src/static/images/{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(image_path)
