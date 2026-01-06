import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import Page
from tests.settings import Settings
from tests.pageobject.pages.board_page import BoardPage


@allure.title("Scenario 1: Urgent Cards Validation")
def test_gui_urgent_card_validation(authenticated_page: Page, settings: Settings):
    """
    1. Login to trello.
    2. Navigate to the Trello Board link provided in Technical Details.
    3. Find all cards with the "Urgent" label across all columns.
    4. For each urgent card, extract and report:
        ○ Card title
        ○ Card description
        ○ Labels
        ○ Current status (To Do, In Progress, Done)
    """

    with allure.step("Open board page"):
        try:
            page = BoardPage(page=authenticated_page, page_url=settings.PAGE_URL_BOARD)
            page.open()
        except Exception as e:
            pytest.fail(f"failed to open page: {e}")

    with allure.step("Capture cards with label 'Urgent'"):
        try:
            urgent_cards = page.urgent_cards
            allure.attach(body="\n".join(str(c) for c in urgent_cards), attachment_type=AttachmentType.TEXT)
            # must have at least one urgent card for this test
            assert urgent_cards, "urgent cards not found"
        except Exception as e:
            pytest.fail(f"failed to locate urgent cards: {e}")

    # report card details for each urgent card
    for card in urgent_cards:
        with allure.step("Open card window"):
            try:
                card_back = card.open()
                # make sure network requests are done
                authenticated_page.wait_for_load_state("networkidle")
            except Exception as e:
                pytest.fail(f"failed to open card: {e}")

        with allure.step("Report card title"):
            try:
                title = card_back.title
                allure.attach(body=title, attachment_type=AttachmentType.TEXT)
            except Exception as e:
                pytest.fail(f"failed to read card title: {e}")

        with allure.step("Report card description"):
            try:
                description = card_back.description if card.has_description else ""
                allure.attach(body=description, attachment_type=AttachmentType.TEXT)
            except Exception as e:
                pytest.fail(f"failed to read card description: {e}")

        with allure.step("Report card labels"):
            try:
                labels = card_back.labels
                allure.attach(body="\n".join(labels), attachment_type=AttachmentType.TEXT)
            except Exception as e:
                pytest.fail(f"failed to read card labels: {e}")

        with allure.step("Report card status"):
            try:
                status = card_back.status
                allure.attach(body=status, attachment_type=AttachmentType.TEXT)
            except Exception as e:
                pytest.fail(f"failed to read card status: {e}")

        with allure.step("Close card window"):
            try:
                card_back.close()
            except Exception as e:
                pytest.fail(f"failed to close card: {e}")
