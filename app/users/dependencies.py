from fastapi import Depends, HTTPException, status

from app.users.auth import get_current_user
from app.users.models import User


async def is_current_user_admin(current_user: User = Depends(get_current_user)):
    if current_user.is_admin or current_user.is_super_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Недостаточно прав!"
    )


async def is_current_user_superadmin(current_user: User = Depends(get_current_user)):
    if current_user.is_super_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Недостаточно прав!"
    )


async def is_current_user_vendor(current_user: User = Depends(get_current_user)):
    if current_user.is_vendor or current_user.is_admin or current_user.is_super_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Недостаточно прав!"
    )


async def is_current_user_analyst(current_user: User = Depends(get_current_user)):
    if current_user.is_analyst or current_user.is_admin or current_user.is_super_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Недостаточно прав!"
    )
