from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field




class CreateTodoRequestModel(BaseModel):
    title : str = Field(...)
    description : str | None = None
    is_completed : bool = False


class CreateTodoResponseModel(BaseModel):
    id : UUID
    title : str
    description : str | None
    is_completed : bool
    created_at : datetime
    updated_at : datetime



class UpdateTodoRequestSchema(BaseModel):
    title : str
    description : str
    is_completed : bool



class UpdateTodoResponseModel(BaseModel):
    id : UUID
    title : str
    description : str | None
    is_completed : bool
    created_at : datetime
    updated_at : datetime
