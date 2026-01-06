import allure
import pytest
from allure_commons.types import AttachmentType
from src.api_clients.gmail_client import GmailClient
from src.api_clients.trello_client import TrelloClient
from src.models.card import Card
from src.utils import cards_by_mail_subj


@allure.title("Scenario: Sync Validation (Urgent Card Labeling)")
def test_api_urgent_card_labeling(gmail_client: GmailClient, trello_client: TrelloClient):
    """
    Urgent Card Labeling: Each "mail" whose body contains the word "Urgent" should
    appear as a card in Trello with the "Urgent" label.
    """

    urgent_kw = "urgent"

    with allure.step("Load cards from Trello API"):
        try:
            card_list = trello_client.card_list
            allure.attach(attachment_type=AttachmentType.TEXT, body="\n".join(str(c) for c in card_list))
        except Exception as e:
            pytest.fail(f"failed to load cards from trello: {e}")

    with allure.step("Load emails from Gmail mock API"):
        try:
            mail_list = gmail_client.mail
            allure.attach(attachment_type=AttachmentType.TEXT, body="\n".join(str(c) for c in mail_list))
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

        with allure.step(f"Verify card found for message '{mail_subj}'"):
            allure.attach(attachment_type=AttachmentType.TEXT, body=str(mail_card_list))

            # email must have a card present
            assert mail_card_list, f"card not found for message {mail_subj}"

        card_urgt_list.extend(mail_card_list)

    with allure.step("Verify at least one urgent card"):
        assert card_urgt_list, "no urgent cards found"

    # iterate over all urgent cards to verify labels
    for cu in card_urgt_list:
        # card labels must include "urgent" label
        with allure.step(f"Verify card labels include 'Urgent'"):
            labels_norm = [l.lower() for l in cu.labels]
            allure.attach(attachment_type=AttachmentType.TEXT, body=str(cu.labels))
            assert urgent_kw in labels_norm, f"expected 'urgent' label in '{labels_norm}'"
