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

    board_page = BoardPage(page=authenticated_page, page_url=settings.PAGE_URL_BOARD)
    board_page.open()

    urgent_cards = board_page.urgent_cards
    # must have at least one urgent card for this test
    assert urgent_cards, "urgent cards not found"

    # report card details for each urgent card
    for card in urgent_cards:
        card_back = card.open()

        title = card_back.title
        description = card_back.description if card.has_description else None
        labels = card_back.labels
        status = card_back.status

        print(f"TITLE:          {title}")
        print(f"DESCRIPTION:    {description}")
        print(f"LABELS:         {labels}")
        print(f"STATUS:         {status}")

        card_back.close()
