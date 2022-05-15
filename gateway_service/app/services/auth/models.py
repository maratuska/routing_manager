from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRead(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    username: str
    password: str
