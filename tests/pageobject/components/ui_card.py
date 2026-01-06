from playwright.sync_api import Page
from playwright.sync_api import Locator
from tests.pageobject.components.ui_card_back import UICardBack


class UICard:
    def __init__(self, page: Page, locator: Locator):
        self.page = page
        self.locator = locator

    @property
    def has_description(self) -> bool:
        desc_elem = self.locator.get_by_test_id("DescriptionIcon")
        return desc_elem.is_visible()

    @property
    def title(self) -> str:
        return self.locator.get_by_test_id("card-name").text_content()

    def open(self) -> UICardBack:
        self.locator.click()
        return UICardBack(self.page)
