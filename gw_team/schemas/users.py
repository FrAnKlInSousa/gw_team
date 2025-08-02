from pydantic import BaseModel, ConfigDict, EmailStr

from gw_team.models.users import UserType


class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    user_type: UserType


class UserPublic(User):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserSchema(User):
    password: str


class UserList(BaseModel):
    users: list[UserPublic]


class UpdateUser(BaseModel):
    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    user_type: UserType | None = None
