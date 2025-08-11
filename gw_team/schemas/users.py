from pydantic import BaseModel, ConfigDict, EmailStr, Field

from gw_team.models.users import UserType


class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    user_type: UserType
    modalities: list[str] = Field(alias='modalities')


class UserPublic(BaseModel):
    id: int
    name: str
    last_name: str
    email: EmailStr
    user_type: UserType
    modalities: list[str] = Field(
        alias='modalities', serialization_alias='modalities'
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserSchema(User):
    password: str


class UserList(BaseModel):
    users: list[UserPublic]
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UpdateUser(BaseModel):
    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    user_type: UserType | None = None


class UpdatePassword(BaseModel):
    new_password: str
