from pydantic import BaseModel, ConfigDict


class Email(BaseModel):
    """
    data model for containing email information (gmail client schema)
    """

    model_config = ConfigDict(extra="ignore")

    date: str
    subject: str
    body: str
    labels: list[str]
