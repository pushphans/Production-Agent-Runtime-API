from uuid import UUID
from datetime import datetime
from pydantic import EmailStr
from pydantic import Field
from pydantic import BaseModel, ConfigDict



class RegisterRequestSchema(BaseModel):
    name : str = Field(...)
    email : EmailStr = Field(..., max_length=100)
    password : str = Field(..., min_length=6)



class RegisterResponseSchema(BaseModel):
    user_id : UUID
    name : str
    email : str
    created_at : datetime
    updated_at : datetime




class LoginRequestSchema(BaseModel):
    email : EmailStr
    password : str



class LoginResponseSchema(BaseModel):
    user_id : UUID
    name : str
    email : str
    access_token : str
    access_token_expiry : int
    refresh_token : str



class RefreshTokenRequestSchema(BaseModel):
    refresh_token : str

class RefreshTokenResponseSchema(BaseModel):
    refresh_token : str
    access_token : str
    access_token_expiry : int
