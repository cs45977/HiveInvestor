from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
