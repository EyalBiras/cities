import uuid
import uvicorn
from fastapi import Request, Depends, HTTPException, Response, FastAPI
from fastapi.responses import RedirectResponse
from models import User, Group
app = FastAPI()
users_db = {}
groups_db = []
SESSION_DB = {}

def get_auth_user(request: Request):
    session_id = request.cookies.get("Authorization")

    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    username = SESSION_DB.get(session_id)
    if not username:
        raise HTTPException(status_code=403, detail="Invalid session")

    return username

@app.post("/signup")
async def signup(username: str, password: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    users_db[username] = User(username=username, password=password, group="none")

    return {"status": "User created successfully"}

@app.post("/create_group", dependencies=[Depends(get_auth_user)])
async def create_group(request:Request, group_name: str):
    username = get_auth_user(request)
    print(users_db[username])
    groups_db.append(Group(name=group_name, members={users_db[username]}))
    print(groups_db)
    return {"status": "User created successfully"}

@app.post("/login")
async def session_login(username: str, password: str):
    if username not in users_db or not password == users_db.get(username).password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid.uuid4())

    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="Authorization", value=session_id)

    SESSION_DB[session_id] = username
    return response

@app.post("/logout")
async def session_logout(response: Response, request: Request):
    session_id = request.cookies.get("Authorization")
    if not session_id or session_id not in SESSION_DB:
        raise HTTPException(status_code=400, detail="No active session found")

    response.delete_cookie(key="Authorization")
    SESSION_DB.pop(session_id, None)

    return {"status": "logged out"}


@app.get("/", dependencies=[Depends(get_auth_user)])
async def secret(request: Request):
    username = get_auth_user(request)
    return {"secret": f"info for {username}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=800)