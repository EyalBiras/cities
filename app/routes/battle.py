import pathlib
from pathlib import Path
from typing import Annotated
import shutil
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from db import groups_db
from models import User
from tournament import battle
from .auth import get_current_active_user

router = APIRouter()
FILE = Path(__file__)
BASE_PATH = FILE.parent.parent.parent / "groups"

battles_requests = set()


def get_group_directory(group: str) -> Path:
    return BASE_PATH / Path(group)


@router.get("/get_groups_to_battle")
async def battle_group(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please join a group before starting a battle!")
    groups_to_battle = []
    for group in groups_db:
        if group.name != current_user.group:
            groups_to_battle.append(group)
    return groups_to_battle


@router.get("/battle/{group_name}")
async def battle_group(
        current_user: Annotated[User, Depends(get_current_active_user)],
        group_name: str):
    if group_name not in [group.name for group in groups_db]:
        raise HTTPException(status_code=400,
                            detail="Please enter a valid group!")
    if current_user.group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please join a group before starting a battle!")
    if current_user.group in battles_requests:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Your group already started a battle!")
    battles_requests.add(current_user.group)
    enemy_group = get_group_directory(group_name)
    user_group = get_group_directory(current_user.group)
    games_directory = user_group / "battles"
    for game in Path(games_directory).glob("*"):
        if group_name in game.name:
            shutil.rmtree(game)
    battle(group=user_group, enemy=enemy_group, games_directory=games_directory)
    battles_requests.remove(current_user.group)


@router.get("/get_battles")
async def get_group_games(current_user: Annotated[User, Depends(get_current_active_user)], ):
    if current_user.group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please be in a group to see battles!")
    if current_user.group not in [group.name for group in groups_db]:
        raise HTTPException(status_code=400,
                            detail="Please enter a valid group!")

    games_directory = Path(f"../groups/{current_user.group}/battles")
    group_battles = []
    for game in games_directory.glob("*"):
        group_battles.append(game.name)
    return group_battles


@router.get("/get_battle/{enemy}")
async def get_battle(
        current_user: Annotated[User, Depends(get_current_active_user)],
        enemy: str
):
    if current_user.group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please be in a group to download battles")
    games_directory = Path(f"../groups/{current_user.group}/battles/")
    games_directory = games_directory / enemy
    group_battle = []
    for game in games_directory.glob("*"):
        group_battle.append(game.name)
    return group_battle

@router.get("/download_battle/{enemy}/{filename}")
async def download_file(
        current_user: Annotated[User, Depends(get_current_active_user)],
        enemy: str,
        filename: str
):
    if current_user.group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please be in a group to download battles")
    games_directory = Path(f"../groups/{current_user.group}/battles/{enemy}")
    game_path = games_directory / Path(filename)
    print(game_path)
    if not game_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(game_path, media_type="application/octet-stream")
