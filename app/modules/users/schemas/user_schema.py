from pydantic import BaseModel , EmailStr , Field

class UserSchema(BaseModel):
    username : str = Field(... ,example="Admin1")
    email: EmailStr =Field(..., example="Admin@gmail.com")
    password: str = Field(..., min_length=6, example="Admin123")



class  CreateEmployeeSchema(BaseModel):
    username: str = Field(..., example="Employeee 1")
    email: EmailStr = Field(...,example="employee@gmail.com")
    password: str = Field(...,min_length=6,example="password1")

