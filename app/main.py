from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.models import User, UserInDB, Group, Token, TokenData
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from app.db import users_db, groups_db, get_group_by_name, get_user
from app.routes import auth, group, file_upload
from app.routes.auth import get_current_active_user
# to get a string like this run:
# openssl rand -hex 32


app = FastAPI()
app.include_router(auth.router)
app.include_router(group.router)
app.include_router(file_upload.router)
app.mount("/static", StaticFiles(directory=r"C:\Users\user\PycharmProjects\cities\app\static"), name="static")



@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/", response_class=HTMLResponse)
async def get_home_page():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/signup.html", response_class=HTMLResponse)
async def get_signup_page():
    with open("static/signup.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/dashboard.html", response_class=HTMLResponse)
async def get_dashboard_page():
    with open("static/dashboard.html") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=900)
