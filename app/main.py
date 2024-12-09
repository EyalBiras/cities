import sys
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from models import User
from routes import auth, group, file_upload, admin, results, battle
from routes.auth import get_current_active_user

# to get a string like this run:
# openssl rand -hex 32


app = FastAPI()
app.include_router(auth.router)
app.include_router(group.router)
app.include_router(file_upload.router)
app.include_router(admin.router)
app.include_router(results.router)
app.include_router(battle.router)
static_directory = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=static_directory), name="static")


@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/", response_class=HTMLResponse)
async def get_home_page():
    with open(static_directory / "index.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/signup.html", response_class=HTMLResponse)
async def get_signup_page():
    with open(static_directory /"signup.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/dashboard.html", response_class=HTMLResponse)
async def get_dashboard_page():
    with open(static_directory /"dashboard.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/files.html", response_class=HTMLResponse)
async def get_files_page():
    with open(static_directory /"files.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/groups.html", response_class=HTMLResponse)
async def get_groups_page():
    with open(static_directory /"groups.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/admin.html", response_class=HTMLResponse)
async def get_admin_page():
    with open(static_directory /"admin.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/results.html", response_class=HTMLResponse)
async def get_results_page():
    with open(static_directory /"results.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/battle.html", response_class=HTMLResponse)
async def get_battle_page():
    with open(static_directory /"battle.html") as f:
        return HTMLResponse(content=f.read())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
