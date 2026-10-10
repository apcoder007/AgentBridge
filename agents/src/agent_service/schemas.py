from pydantic import BaseModel, Field


class InvokeRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)
    agent_id: str = Field(default="joke", min_length=1, max_length=100)


class InvokeResponse(BaseModel):
    response: str
