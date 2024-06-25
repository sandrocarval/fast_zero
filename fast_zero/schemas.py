from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr


class UserListSchema(BaseModel):
    users: list[UserSchema]


class DBUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class SubmitUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
