import pytest
from src.api_clients.gmail_client import GmailClient
from src.api_clients.trello_client import TrelloClient
from src.models.email import Email
from src.utils import parse_date, cards_by_mail_subj


def test_sync_merge_api(gmail_client: GmailClient, trello_client: TrelloClient):
    """
    Merging: When there are some "emails" with the same subject (and different body),
    they must appear as one card in Trello, with the bodies concatenated in the description.

    1. Mail 1: subject: "Hello", body: "To you"
    2. Mail 2: subject: "Hello", body: "my friend"
    3. Trello: a card with title "Hello" and description:
    "To you
    my friend".
    """

    try:
        card_list = trello_client.card_list
    except Exception as e:
        pytest.fail(f"failed to load cards from trello: {e}")

    try:
        mail_list = gmail_client.mail
    except Exception as e:
        pytest.fail(f"failed to load mails from gmail: {e}")

    # group email lists by their subjects
    subj_mail_map: dict[str, list[Email]] = {}
    for mail in mail_list:
        mail_sub = mail.subject
        if mail_sub not in subj_mail_map.keys():
            subj_mail_map[mail_sub] = []
        subj_mail_map[mail_sub].append(mail)

    # iterate email groups to find merging test candidates
    for mail_sub, mail_lst in subj_mail_map.items():
        if len(mail_lst) < 2:
            # at least 2 emails with similar subject for merge test
            continue

        mail_card_list = cards_by_mail_subj(card_list, mail_sub)

        # email subject must have exactly one card
        card_list_l = len(mail_card_list)
        assert card_list_l == 1, f"found {card_list_l} cards for subject {mail_sub}"

        # concatenate email bodies separated by new line
        exp_card_desc = "\n".join(m.body for m in sorted(mail_lst, key=parse_date))

        # card description must match concatenated email bodies
        act_card_desc = mail_card_list[0].desc
        assert act_card_desc == exp_card_desc, f"expected description '{exp_card_desc}'. got '{act_card_desc}'"
