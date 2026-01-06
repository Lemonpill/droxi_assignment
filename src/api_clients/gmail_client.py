import json
from pathlib import Path
from src.models.email import Email


class GmailClient:
    def __init__(self, path: Path):
        self.path = path

    @property
    def mail(self):
        with open(self.path) as file:
            data = json.load(file)
        return [Email(**e) for e in data.get("messages")]
