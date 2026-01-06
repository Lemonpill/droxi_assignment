import requests
from src.models.card import Card


class TrelloClient:
    def __init__(self, api_key: str, api_token: str, endpoint: str):
        self.api_key = api_key
        self.api_token = api_token
        self.endpoint = endpoint

    @property
    def card_list(self):
        resp = requests.get(self.endpoint, params={"key": self.api_key, "token": self.api_token})
        resp_json = resp.json()

        cards: list[Card] = []
        for c in resp_json:
            name = c.get("name")
            description = c.get("desc")
            labels = [l.get("name") for l in c.get("labels")]
            cards.append(
                Card(
                    name=name,
                    desc=description,
                    labels=labels,
                )
            )
        return cards
