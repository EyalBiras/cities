from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.models import User, UserInDB, Group
from app.routes.auth import get_current_active_user
from app.db import users_db, groups_db, get_user, get_group_by_name
from fastapi import Form
import tournament

router = APIRouter()

@router.post("/run_tournament")
async def run_tournament(current_user: Annotated[User, Depends(get_current_active_user)],):
    if current_user.username != "Admin":
        raise HTTPException(status_code=400,
                            detail=f"Error")

    tournament.run_tournament()
