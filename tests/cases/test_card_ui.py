import pytest
from playwright.sync_api import Page
from tests.settings import Settings
from tests.pageobject.pages.board_page import BoardPage


def test_card_ui(authenticated_page: Page, settings: Settings):
    """
    1. Login to trello.
    2. Navigate to the Trello Board link provided in Technical Details.
    3. Locate and open the "summarize the meeting" card from the board view.
    4. Extract and validate card details:
        ○ Card title: Verify it matches "summarize the meeting".
        ○ Description: Verify description text matches exactly: "For all of us. Please do so".
        ○ Labels: Extract all labels and verify the "New" label is present.
        ○ Current status: Verify the card is in the "To Do" column.
    5. Close the card modal and return to board view.
    """

    # expected card details
    exp_title = "summarize the meeting"
    exp_description = "For all of us. Please do so"
    exp_label = "New"
    exp_status = "To Do"

    try:
        page = BoardPage(page=authenticated_page, page_url=settings.PAGE_URL_BOARD)
        page.open()
    except Exception as e:
        pytest.fail(f"failed to open page: {e}")

    # locate and open card by expected status and name
    try:
        card = page.get_list_card(list_name=exp_status, card_name=exp_title)
        card_back = card.open()
    except Exception as e:
        pytest.fail(f"failed to open card: {e}")

    try:
        act_title = card_back.title
    except Exception as e:
        pytest.fail(f"failed to read card title: {e}")

    try:
        act_description = card_back.description
    except Exception as e:
        pytest.fail(f"failed to read card description: {e}")

    try:
        act_labels = card_back.labels
    except Exception as e:
        pytest.fail(f"failed to read card labels: {e}")

    try:
        act_status = card_back.status
    except Exception as e:
        pytest.fail(f"failed to read card status: {e}")

    # card title must match the expected
    assert act_title == exp_title, f"expected title '{exp_title}'. got '{act_title}'"

    # card description must match the expected
    assert act_description == exp_description, f"expected description '{exp_description}'. got '{act_description}'"

    # card must include the expected label
    assert exp_label in act_labels, f"expected label '{exp_label}' in '{act_labels}'"

    # card status must be equal expected status
    assert act_status == exp_status, f"expected status '{exp_status}'. got '{act_status}'"

    try:
        card_back.close()
    except Exception as e:
        pytest.fail(f"failed to close card: {e}")
