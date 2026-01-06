import os
import shlex
from datetime import datetime
from typing import Any
from urllib.parse import urlparse
from src.models.email import Email
from src.models.card import Card


def parse_curl(curl_cmd: str) -> tuple[str | None, dict, dict]:
    """
    parse curl to extract url, headers and cookies
    """

    tokens = shlex.split(curl_cmd)
    headers = {}
    cookies = {}
    url = None
    it = iter(tokens)
    for token in it:
        if token.lower() == "curl":
            continue
        if token in ("-H", "--header"):
            h = next(it)
            k, v = h.split(":", 1)
            headers[k.strip()] = v.strip()
        elif token in ("-b", "--cookie"):
            cookie_str = next(it)
            for c in cookie_str.split(";"):
                if "=" in c:
                    k, v = c.strip().split("=", 1)
                    cookies[k] = v
        elif token.startswith("http"):
            url = token
    if "cookie" in headers:
        for c in headers["cookie"].split(";"):
            if "=" in c:
                k, v = c.strip().split("=", 1)
                cookies[k] = v
        del headers["cookie"]
    return url, headers, cookies


def cookies_for_playwright(cookies: dict, url: str) -> list[dict[str, Any]]:
    """
    create cookies compatible with playwright
    """

    parsed = urlparse(url)
    domain = parsed.hostname
    return [{"name": k, "value": v, "domain": domain if domain.startswith(".") else f".{domain}", "path": "/", "secure": True, "httpOnly": False} for k, v in cookies.items()]


def build_test_curl():
    """
    build curl string to avoid 2fa
    """

    PAGE_URL_BOARD = os.getenv("PAGE_URL_BOARD", "https://trello.com/b/2GzdgPlw/droxi")
    ATLASSIAN_ACCOUNT_XSRF_TOKEN = os.getenv("ATLASSIAN_ACCOUNT_XSRF_TOKEN", "")
    CLOUD_SESSION_TOKEN = os.getenv("CLOUD_SESSION_TOKEN", "")
    curl = f"""curl '{PAGE_URL_BOARD}' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cache-control: max-age=0' \
  -b 'dsc=a98d3d5bc7021a1d8bd69f83527afab35e6beb558906c1eb90bdc7d2a35c1981; lang=he-IL; hasAccount=atlassian; atl-bsc-consent-token=0030000111; atl-bsc-show-banner=1; atlassian.account.xsrf.token={ATLASSIAN_ACCOUNT_XSRF_TOKEN}; loggedIn=1; aaId=712020%3A16cc22c5-6f08-40c8-84f7-324c13d78f2f; idMember=6772b243eeb4f4b07ea38c4c; __cid=9PC0khAWNGUQvyhazB5oqYbXcnRp-yG5VOcUpEPjd8F6r1O6B8GapFU2HQx6_iqsaetYXFOpHdkIL7jzUpSMpl-5E6QognDpOJx2yDuHMJF51j-MAI9xwDiRbIQZsj-VZ8gvn3exdsph0iSEL9ArjXenb9Q7g0jBNa120HjTLJN51SmEf61X8BqqM4Q7j3TBd6F6xzyJNoQUjm3LOoMwlWPVMZR51jGUd7V-wjaUdoti1SiKZNBzrGWELcFlhSqdIOUYL1dyF5Zi13rHZNYoOA-nUeMboz-MHohrwTvKP-05knrIf7Q2hB6Udtd_tDaED4M_4yWHb8w-hWyEf9ZnlGfWL50W0iaNd6J21jKFa5cT1y6EIZVAkQjWP9QkuSr7Z8o_4GSiLpV-QguVeNcwlW7RL4h31CWUZ9wvlHenUgtf5qqFklaKb1c1HnnUsPikvOXo-4_LTpao5FdkV-YfpFfmH6RX5h-kV-YfpFfmH6RX5h-kV-YfpFfmH6RXpl_kF6ZfpFfmH6RX5h-kV-Yf5FfmH6RX5h-kV-YfWw; cloud.session.token={CLOUD_SESSION_TOKEN}' \
  -H 'priority: u=0, i' \
  -H 'referer: https://trello.com/client-side-redirect?returnUrl=%2Fb%2F2GzdgPlw%2Fdroxi' \
  -H 'sec-ch-ua: "Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'"""
    return curl


def parse_date(e: Email):
    """
    date parsing for gmail format
    """

    return datetime.strptime(e.date, "%a, %d %b %Y %H:%M:%S %z")


def cards_by_mail_subj(cards: list[Card], email_sub: str):
    """
    find cards by title from email subject
    """

    card_list: list[Card] = []
    mail_title = email_sub.replace("Task: ", "")
    for card in cards:
        card_title = card.name
        if mail_title != card_title:
            continue
        card_list.append(card)
    return card_list
