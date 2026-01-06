"""
Merging: When there are some "emails" with the same subject (and different body),
they must appear as one card in Trello, with the bodies concatenated in the description.

1. Mail 1: subject: "Hello", body: "To you"
2. Mail 2: subject: "Hello", body: "my friend"
3. Trello: a card with title "Hello" and description:
"To you
my friend".
"""

import pytest
from src.api_clients.gmail_client import GmailClient
from src.api_clients.trello_client import TrelloClient
from src.models.email import Email
from src.utils import parse_date


def test_sync_merge_api(gmail_client: GmailClient, trello_client: TrelloClient):

    card_list = trello_client.card_list
    mail_list = gmail_client.mail

    subj_mail_map: dict[str, list[Email]] = {}

    for mail in mail_list:
        mail_sub = mail.subject
        if mail_sub not in subj_mail_map.keys():
            subj_mail_map[mail_sub] = []
        subj_mail_map[mail_sub].append(mail)

    for mail_sub, mail_lst in subj_mail_map.items():
        if len(mail_lst) < 2:
            continue
        mail_card = None
        for card in card_list:
            if card.name != mail_sub.replace("Task: ", ""):
                continue
            if mail_card:
                pytest.fail(f"duplicated: {mail_card}")
            mail_card = card
        if not mail_card:
            pytest.fail(f"card not found {mail_sub}")
        exp_card_desc = "\n".join(m.body for m in sorted(mail_lst, key=parse_date))
        assert mail_card.desc == exp_card_desc
