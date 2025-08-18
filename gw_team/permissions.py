from http import HTTPStatus

from fastapi import HTTPException

from gw_team.models.models import User


async def check_permission(user: User, user_id: int) -> None:
    if user.id != user_id and not user.is_admin:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='You have no permission'
        )


async def check_admin_permission(user: User) -> None:
    if not user.is_admin:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='You have no permission'
        )
