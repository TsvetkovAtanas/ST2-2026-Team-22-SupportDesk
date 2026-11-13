from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    company: str = Field(min_length=1, max_length=100)

    @field_validator("phone_number", mode="before")
    @classmethod
    def empty_phone_number_to_none(cls, value):
        if isinstance(value, str) and not value.strip():
            return None
        return value
    