import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    parses / validates settings from environment variables
    """

    PAGE_URL_BOARD: str = os.getenv("PAGE_URL_BOARD")
    ATLASSIAN_ACCOUNT_XSRF_TOKEN: str = os.getenv("ATLASSIAN_ACCOUNT_XSRF_TOKEN")
    CLOUD_SESSION_TOKEN: str = os.getenv("CLOUD_SESSION_TOKEN")
    TEST_HEADLESS: bool = os.getenv("TEST_HEADLESS")
    TRELLO_API_KEY: str = os.getenv("TRELLO_API_KEY")
    TRELLO_API_TOKEN: str = os.getenv("TRELLO_API_TOKEN")
    TRELLO_API_EP: str = os.getenv("TRELLO_API_URL")
