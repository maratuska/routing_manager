from typing import Optional

from pydantic.main import BaseModel
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint


class BaseUser(SQLModel):
    username: str


class User(BaseUser, table=True):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('username'), )

    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str


class UserCreate(BaseUser):
    password: str


class UserAuth(BaseUser):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
