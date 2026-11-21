from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import Priority, Category

class TicketIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    priority: Priority = Field(default=Priority.MEDIUM)
    category: Category = Field(default=Category.OTHER)
    customer_id: int
    assigned_agent_id: int
