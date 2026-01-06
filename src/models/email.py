from pydantic import BaseModel, ConfigDict


class Email(BaseModel):
    model_config = ConfigDict(extra="ignore")

    date: str
    subject: str
    body: str
    labels: list[str]
