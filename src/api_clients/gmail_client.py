import json
from pathlib import Path
from src.models.email import Email


class GmailClient:
    """
    gmail client: mock client working with local file path to fetch mailbox
    """

    def __init__(self, path: Path):
        self.path = path

    @property
    def mail(self):
        # load raw emails
        with open(self.path) as file:
            data = json.load(file)
        # return validated and parsed models
        return [Email(**e) for e in data.get("messages")]
