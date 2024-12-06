import zipfile
from pathlib import Path
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi import BackgroundTasks

from app.models import User
from app.routes.auth import get_current_active_user
import uvicorn
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
DEVELOPMENT_CODE_DIR = "development_code"
ONE_MEGABYTE = 1048576
MAX_SIZE = ONE_MEGABYTE
MAX_SIZE_STR = "1mb"
MAX_AMOUNT_OF_FILES = 40
router = APIRouter()
BASE_PATH = Path("../groups")


def is_hidden_file(file: Path) -> bool:
    if file.name.endswith("pyc"):
        return True
    if file.name[-1] == "_":
        return True

def get_group_directory(group: str) -> Path:
    return BASE_PATH / Path(group)


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
        if is_hidden_file(Path(file.filename)):
            raise HTTPException(status_code=400,
                                detail=f"File shouldn't end with pyc or _")

    for file in files:
        file_path = get_group_directory(current_user.group) / DEVELOPMENT_CODE_DIR / file.filename

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        file_locations.append(file.filename)

    return {"message": "Files uploaded successfully", "files": file_locations}


@router.get("/download_file/{filename}")
async def download_file(
        current_user: Annotated[User, Depends(get_current_active_user)],
        filename: str
):
    if current_user.group is None:
        raise HTTPException(status_code=400,
                            detail=f"You need to be in a group inorder to download files")

    file_path = get_group_directory(current_user.group) / DEVELOPMENT_CODE_DIR / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


@router.get("/download_all/")
async def download_all_files(
        current_user: Annotated[User, Depends(get_current_active_user)],
        background_tasks: BackgroundTasks):
    if current_user.group is None:
        raise HTTPException(status_code=400,
                            detail=f"You need to be in a group inorder to download files")

    group_directory = get_group_directory(current_user.group) / DEVELOPMENT_CODE_DIR

    if not group_directory.exists():
        raise HTTPException(status_code=404, detail="No files have been uploaded")

    zip_filename = f"{current_user.group}.zip"
    zip_file_path = Path("/tmp") / zip_filename
    zip_file_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'w') as zip_stream:
        for file_path in group_directory.rglob("*"):
            if is_hidden_file(file_path):
                continue
            if file_path.is_file():
                zip_stream.write(file_path, file_path.relative_to(group_directory))

    background_tasks.add_task(delete_file, zip_file_path)

    return FileResponse(zip_file_path, media_type="application/zip", filename=zip_filename)


@router.get("/list_all")
async def get_files(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.group is None:
        raise HTTPException(status_code=400,
                            detail=f"You need to be in a group inorder to download files")

    group_directory = get_group_directory(current_user.group) / DEVELOPMENT_CODE_DIR
    if not group_directory.exists():
        return []
    files = []
    for file_path in group_directory.rglob("*"):
        if is_hidden_file(file_path):
            continue
        files.append(Path(file_path).name)
    return files


def delete_file(file_path: Path):
    file_path.unlink()
