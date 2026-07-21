from pydantic import BaseModel, Field


class parser(BaseModel):
    path = Field(..., description="Path to the functions definition JSON file")
