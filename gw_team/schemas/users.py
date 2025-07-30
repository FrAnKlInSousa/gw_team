from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr


class UserPublic(User):
    id: int


class UserSchema(User):
    password: str
