from pydantic import BaseModel


class Card(BaseModel):
    """
    data model for containing card information (trello client schema)
    """

    name: str
    desc: str
    labels: list[str]
