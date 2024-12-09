import json
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from db import groups_db
from models import User
from .auth import get_current_active_user
file = Path(__file__)
RESULTS_FILE = file.parent.parent.parent / "results.json"
GAMES_DIRECTORY = file.parent.parent.parent / "games"

router = APIRouter()

@router.get("/get_tournament_results")
async def get_tournament_results(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    with open(RESULTS_FILE) as f:
        results = json.load(f)
    sorted_results = sorted(results.items(), key=lambda x: x[1]["total score"], reverse=True)
    print(sorted_results)
    return dict(sorted_results)

@router.get("/get_group_games/{group_name}")
async def get_group_games(group_name: str):
    if group_name not in [group.name for group in groups_db]:
        raise HTTPException(status_code=400,
                            detail="Please enter a valid group!")

    group_games = []
    for game in GAMES_DIRECTORY.glob("*"):
        if group_name in game.name:
            group_games.append(game.name)
    return group_games

@router.get("/download_game/{filename}")
async def download_file(
    filename: str
):
    game_path = GAMES_DIRECTORY / Path(filename)
    if not game_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")


    return FileResponse(game_path, media_type="application/octet-stream", filename=filename)