from playwright.sync_api import Page


class UICardBack:
    def __init__(self, page: Page):
        self.page = page
        self.locator = page.get_by_test_id("card-back-name")

    @property
    def title(self) -> str:
        return self.locator.get_by_test_id("card-back-title-input").text_content()

    @property
    def description(self) -> str:
        return self.locator.get_by_test_id("description-content-area").inner_text()

    @property
    def labels(self) -> list[str]:
        elems = self.locator.get_by_test_id("card-label").all()
        return [e.inner_text() for e in elems]

    @property
    def status(self) -> str:
        return self.locator.locator("//header//button[@title]").get_attribute("title")

    @property
    def is_visible(self) -> bool:
        return self.locator.is_visible()

    def close(self):
        return self.locator.get_by_role("button", name="Close dialog").click()
