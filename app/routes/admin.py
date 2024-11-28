from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

import tournament
from app.models import User
from app.routes.auth import get_current_active_user

router = APIRouter()


@router.post("/run_tournament")
async def run_tournament(current_user: Annotated[User, Depends(get_current_active_user)], ):
    if current_user.username != "Admin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")

    tournament.run_tournament()
