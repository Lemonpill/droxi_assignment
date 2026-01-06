from playwright.sync_api import Page
from tests.pageobject.components.ui_card import UICard


class BoardPage:
    def __init__(self, page: Page, page_url: str):
        self.page = page
        self.page_url = page_url

    @property
    def urgent_cards(self) -> list[UICard]:
        self.page.wait_for_selector('[data-testid="list-wrapper"] [data-testid="trello-card"]')
        label_locator = self.page.get_by_test_id("compact-card-label").filter(has_text="Urgent")
        cards_locator = self.page.get_by_test_id("trello-card").filter(has=label_locator)
        return [UICard(self.page, locator) for locator in cards_locator.all()]

    def get_list_card(self, list_name: str, card_name: str):
        card_list_locator = self.page.get_by_test_id("list-wrapper").filter(has_text=list_name)
        card_locator = card_list_locator.get_by_test_id("trello-card").filter(has_text=card_name).first
        return UICard(page=self.page, locator=card_locator)

    def open(self):
        self.page.goto(self.page_url)
        self.page.wait_for_load_state("networkidle")
