from pydantic import BaseModel, ConfigDict


class MessageResponse(BaseModel):
    message: str


class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int


class ErrorResponse(BaseModel):
    error: str
    details: dict = {}


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
