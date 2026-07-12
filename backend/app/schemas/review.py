from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ReviewCreate(BaseModel):
    title: str = Field(min_length = 2,max_length = 255)
    rating: int = Field(
    ge=1,
    le=5,
)
    feedback: str = Field(min_length = 1)

class ReviewResponse(BaseModel):
    id: int
    title: str
    rating: int
    feedback: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReviewUpdate(BaseModel):
    title: str = Field(min_length = 2,max_length = 255)
    rating: int = Field(ge=1,le=5,)
    feedback: str = Field(min_length = 1)

class MessageResponse(BaseModel):
    message: str