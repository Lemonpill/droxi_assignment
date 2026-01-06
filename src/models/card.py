from pydantic import BaseModel


class Card(BaseModel):
    name: str
    desc: str
    labels: list[str]
