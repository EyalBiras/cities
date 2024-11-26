from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.models import User, UserInDB, Group
from app.routes.auth import get_current_active_user
from app.db import users_db, groups_db, get_user, get_group_by_name
from fastapi import Form

router = APIRouter()

@router.post("/create_group")
async def create_group(
        current_user: Annotated[User, Depends(get_current_active_user)],
        group_name: str = Form(...)
):
    if current_user.group is not None:
        raise HTTPException(status_code=400,
                            detail=f"You are already in a group {current_user.group}, leave the group inorder to create a new one")
    if group_name in [group.name for group in groups_db]:
        raise HTTPException(status_code=400,
                            detail=f"A group with name {group_name} already exists please choose a different name")
    get_user(current_user.username)["group"] = group_name
    groups_db.append(Group(name=group_name, members=[current_user.username], owner=current_user.username, join_requests=[]))



@router.post("/leave_group")
async def leave_group(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.group is None:
        raise HTTPException(status_code=400, detail=f"You are not in a group!")
    for group in groups_db:
        if group.name == current_user.group:
            group.members.remove(current_user.username)
            if len(group.members) == 0:
                groups_db.remove(group)
                break
            if group.owner == current_user.username:
                group.owner = group.members[0]
            break
    get_user(current_user.username)["group"] = None
    return {"message": "Left group successfully"}


@router.get("/groups")
async def get_groups():
    return groups_db


@router.post("/join_request")
async def send_join_request(
        current_user: Annotated[User, Depends(get_current_active_user)],
        group_name: str = Form(...)
):
    if group_name not in [group.name for group in groups_db]:
        raise HTTPException(status_code=400, detail=f"Group {group_name} doesnt exist")
    if current_user.group == group_name:
        raise HTTPException(status_code=400, detail=f"You are already in that group")
    if current_user.group is not None:
        raise HTTPException(status_code=400,
                            detail=f"You are already in a group {current_user.group}, you must leave your group inorder to join to a new one")
    for group in groups_db:
        if group.name == group_name:
            if current_user.username in group.join_requests:
                raise HTTPException(status_code=400,
                                    detail=f"You've are already sent a join request to group {group_name}")
            group.join_requests.append(current_user.username)
    return {"message": "Sent a join request successfully"}


@router.get("/get_join_requests")
async def get_join_requests(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.group is None:
        raise HTTPException(status_code=400, detail=f"You are not in a group")
    for group in groups_db:
        if group.name == current_user.group:
            return group.join_requests

@router.post("/accept_join_request")
async def accept_join_request(
        current_user: Annotated[User, Depends(get_current_active_user)],
        user: str = Form(...)
):
    if current_user.group is None:
        raise HTTPException(status_code=400, detail=f"You are not in a group")
    user_group = get_group_by_name(current_user.group)
    if user_group.owner != current_user.username:
        raise HTTPException(status_code=400, detail=f"You are not the owner of the group {user_group.name}")
    if user not in user_group.join_requests:
        raise HTTPException(status_code=400, detail=f"Invalid accept, the user {user} didn't ask for joining")
    user_group.members.append(user)

    get_user(user)["group"] = user_group.name
    for group in groups_db:
        if user in group.join_requests:
            group.join_requests.remove(user)

    return {"message": f"Added {user} successfully"}