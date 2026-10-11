from pydantic import BaseModel


class ChatRequestSchema(BaseModel):
    message : str


class ChatResponseSchema(BaseModel):
    response : str