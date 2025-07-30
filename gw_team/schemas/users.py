from pydantic import BaseModel
from pydantic import EmailStr


class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr


class UserPublic(User):
    id: int


class UserSchema(User):
    password: str
