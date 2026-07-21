from pydantic import BaseModel, Field
import json


class parser(BaseModel):
    path = Field(..., description="Path to the functions definition JSON file")
