import pytest
from playwright.sync_api import Page
from tests.settings import Settings
from tests.pageobject.pages.board_page import BoardPage


def test_card_urgent_ui(authenticated_page: Page, settings: Settings):
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

    try:
        page = BoardPage(page=authenticated_page, page_url=settings.PAGE_URL_BOARD)
        page.open()
    except Exception as e:
        pytest.fail(f"failed to open page: {e}")

    try:
        urgent_cards = page.urgent_cards
    except Exception as e:
        pytest.fail(f"failed to locate urgent cards: {e}")

    # must have at least one urgent card for this test
    assert urgent_cards, "urgent cards not found"

    # report card details for each urgent card
    for card in urgent_cards:
        try:
            card_back = card.open()
        except Exception as e:
            pytest.fail(f"failed to open card: {e}")

        try:
            title = card_back.title
        except Exception as e:
            pytest.fail(f"failed to read card title: {e}")

        try:
            description = card_back.description if card.has_description else None
        except Exception as e:
            pytest.fail(f"failed to read card description: {e}")

        try:
            labels = card_back.labels
        except Exception as e:
            pytest.fail(f"failed to read card labels: {e}")

        try:
            status = card_back.status
        except Exception as e:
            pytest.fail(f"failed to read card status: {e}")

        print(f"TITLE:          {title}")
        print(f"DESCRIPTION:    {description}")
        print(f"LABELS:         {labels}")
        print(f"STATUS:         {status}")

        try:
            card_back.close()
        except Exception as e:
            pytest.fail(f"failed to close card: {e}")
