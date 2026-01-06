import os
import pytest
import allure
from dotenv import load_dotenv
from pydantic import ValidationError
from playwright.sync_api import sync_playwright
from src.utils import parse_curl, cookies_for_playwright, build_test_curl
from .settings import Settings
from src.api_clients.gmail_client import GmailClient
from src.api_clients.trello_client import TrelloClient


load_dotenv()


@pytest.fixture(scope="session")
def settings():
    """
    validates and returns system settings
    """

    try:
        return Settings()
    except ValidationError as e:
        pytest.exit(f"missing settings in .env: {e}")
    except:
        pytest.exit("failed to load settings")


@pytest.fixture(scope="session")
def authenticated_page(settings: Settings):
    """
    creates an authenticated playwright session from curl
    """

    curl = build_test_curl()
    url, headers, cookies = parse_curl(curl)
    cookies = cookies_for_playwright(cookies=cookies, url=url)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.TEST_HEADLESS)
        context = browser.new_context(extra_http_headers=headers)
        context.add_cookies(cookies)
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def gmail_client():
    """
    configures mock gmail client component
    """

    repo_root = os.path.dirname(os.path.dirname(__file__))
    data_file = os.path.join(repo_root, "data", "mock_gmail_data.json")
    return GmailClient(data_file)


@pytest.fixture(scope="session")
def trello_client(settings: Settings):
    """
    configures trello client component
    """

    return TrelloClient(
        api_key=settings.TRELLO_API_KEY,
        api_token=settings.TRELLO_API_TOKEN,
        endpoint=settings.TRELLO_API_EP,
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    attaches page source and screenshot to allure report in case a test fails
    """

    outcome = yield
    rep = outcome.get_result()
    if not rep.when == "call" or not rep.failed:
        return
    page = item.funcargs.get("authenticated_page")
    if not page:
        return
    png = page.screenshot(full_page=True)
    allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
