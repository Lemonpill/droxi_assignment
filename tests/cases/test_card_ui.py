from playwright.sync_api import Page
from tests.settings import Settings
from tests.pageobject.pages.board_page import BoardPage


def test_card_ui(authenticated_page: Page, settings: Settings):
    exp_title = "summarize the meeting"
    exp_description = "For all of us. Please do so"
    exp_label = "New"
    exp_status = "To Do"

    page = BoardPage(page=authenticated_page, page_url=settings.PAGE_URL_BOARD)
    page.open()

    card = page.get_list_card(list_name=exp_status, card_name=exp_title)
    assert card.title == exp_title

    card_back = card.open()

    act_title = card_back.title
    act_description = card_back.description
    act_labels = card_back.labels
    act_status = card_back.status

    assert act_title == exp_title
    assert act_description == exp_description
    assert exp_label in act_labels
    assert act_status == exp_status

    card_back.close()
