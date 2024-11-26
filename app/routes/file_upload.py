from pathlib import Path
from typing import Annotated
from fastapi.staticfiles import StaticFiles

from app.models import User
from app.routes.auth import get_current_active_user
import uvicorn
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
ONE_MEGABYTE = 1048576
MAX_SIZE = ONE_MEGABYTE
MAX_SIZE_STR = "1mb"
MAX_AMOUNT_OF_FILES = 40
router = APIRouter()

@router.post("/uploadfile/")
async def create_upload_file(
        current_user: Annotated[User, Depends(get_current_active_user)],
        files: list[UploadFile]):

    if current_user.group is None:
        raise HTTPException(status_code=400,
                            detail=f"You need to be in a group inorder to upload files")

    if len(files) > MAX_AMOUNT_OF_FILES:
        raise HTTPException(status_code=400,
                            detail=f"You tried to upload more than {MAX_AMOUNT_OF_FILES}")

    file_locations = []
    total_size = 0
    for file in files:
        if file.size > MAX_SIZE:
            raise HTTPException(status_code=400,
                                detail=f"file {file.filename} exceeds maximum size of {MAX_SIZE_STR}")
        total_size += file.size
        if total_size > MAX_SIZE:
            raise HTTPException(status_code=400,
                                detail=f"Total size of files exceeds maximum size of {MAX_SIZE_STR}")

    for file in files:
        file_path = Path(current_user.group) / file.filename

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

        file_locations.append(file.filename)

    return {"message": "Files uploaded successfully", "files": file_locations}