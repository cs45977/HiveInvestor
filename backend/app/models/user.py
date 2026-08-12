from pydantic import BaseModel, EmailStr
from typing import Literal

Role = Literal["user", "admin"]

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    role: Role = "user"

class UserRoleUpdate(BaseModel):
    role: Role
