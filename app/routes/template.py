from pathlib import Path

from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter()
FILE = Path(__file__)
TEMPLATE_FILE = FILE.parent.parent.parent / "Template.rar"


@router.get("/download_template")
async def download_template(
):
    return FileResponse(TEMPLATE_FILE, media_type="application/octet-stream", filename=TEMPLATE_FILE.name)
