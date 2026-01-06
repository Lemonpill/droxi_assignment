import pytest
from src.api_clients.gmail_client import GmailClient
from src.api_clients.trello_client import TrelloClient
from src.models.card import Card
from src.utils import cards_by_mail_subj


def test_sync_api(gmail_client: GmailClient, trello_client: TrelloClient):
    """
    Urgent Card Labeling: Each "mail" whose body contains the word "Urgent" should
    appear as a card in Trello with the "Urgent" label.
    """

    urgent_kw = "urgent"

    try:
        card_list = trello_client.card_list
    except Exception as e:
        pytest.fail(f"failed to load cards from trello: {e}")

    try:
        mail_list = gmail_client.mail
    except Exception as e:
        pytest.fail(f"failed to load mails from gmail: {e}")

    # iterate emails to find urgent ones
    card_urgt_list: list[Card] = []
    for mail in mail_list:
        mail_subj = mail.subject
        mail_body = mail.body
        is_urgent = urgent_kw in mail_body.lower()

        if not is_urgent:
            # not urgent = not relevant
            continue

        mail_card_list = cards_by_mail_subj(card_list, mail_subj)

        # email must have a card present
        assert mail_card_list, f"card not found for message {mail_subj}"

        card_urgt_list.extend(mail_card_list)

    # iterate over all urgent cards to verify labels
    for cu in card_urgt_list:
        # card labels must include "urgent" label
        assert cu and urgent_kw in [l.lower() for l in cu.labels], f"expected 'urgent' label in '{cu.labels}'"
