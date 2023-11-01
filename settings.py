from pydantic import BaseModel, Field


class Token(BaseModel):
    authjwt_secret_key: str = Field(default='fake-access-token')
