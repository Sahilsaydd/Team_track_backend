from pydantic import BaseModel , EmailStr, Field 


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="password123")

    