from pydantic import BaseModel, ConfigDict, Field

class CommentIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    body: str = Field(min_length=1)