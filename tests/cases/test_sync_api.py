import pytest
from src.api_clients.gmail_client import GmailClient
from src.api_clients.trello_client import TrelloClient
from src.models.card import Card


def test_sync_api(gmail_client: GmailClient, trello_client: TrelloClient):
    urgent_kw = "urgent"

    card_list = trello_client.card_list
    mail_list = gmail_client.mail

    card_urgt_list: list[Card] = []

    for mail in mail_list:
        mail_subj = mail.subject
        mail_body = mail.body
        is_urgent = urgent_kw in mail_body.lower()
        mail_card = None
        if not is_urgent:
            continue
        for card in card_list:
            mail_title = mail_subj.replace("Task: ", "")
            card_title = card.name
            if mail_title != card_title:
                continue
            mail_card = card
            break
        if not mail_card:
            pytest.fail(f"no card for message {mail}")
        card_urgt_list.append(mail_card)

    for cu in card_urgt_list:
        assert cu and urgent_kw in [l.lower() for l in cu.labels]
