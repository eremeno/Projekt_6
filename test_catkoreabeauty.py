"""
Projekt: Tři automatizované testy
"""

import os
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

URL = "https://catkoreabeauty.de/"

COOKIE_BTN_SELECTOR = "button:has-text('Accept all')"
SHOP_LINK_SELECTOR = "#menu-item-27193 > a > span"
SEARCH_ICON_SELECTOR = "div.wd-header-search a"
SEARCH_INPUT_SELECTOR = "input.s.wd-search-inited"
SEARCH_RESULTS_SELECTOR = "h1"


@pytest.fixture(scope="session")
def browser() -> Browser:
    """
    Fixture pro spuštění instance Chromium browseru.
    Parametry headless režimu a slow_mo lze konfigurovat
    pomocí environmentálních proměnných:
        HEADLESS=true/false
        SLOW_MO=milisekundy
    """
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    slow_mo = int(os.getenv("SLOW_MO", "2000"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    """
    Fixture pro vytvoření nové stránky (Page).
    Otevře domovskou stránku a pokud se objeví cookie lišta,
    klikne na tlačítko pro přijetí cookies.
    """
    context: BrowserContext = browser.new_context()
    page: Page = context.new_page()
    page.goto(URL)

    try:
        page.wait_for_selector(COOKIE_BTN_SELECTOR, timeout=3000)
        page.locator(COOKIE_BTN_SELECTOR).click()
    except Exception:
        pass

    yield page
    context.close()


def test_homepage_title(page: Page) -> None:
    """
    Ověří, že domovská stránka má v titulku text 'Catkoreabeauty'.
    
    Args:
        page (Page): Otevřená stránka.
    """
    assert "Catkoreabeauty" in page.title()


def test_navigation_to_shop(page: Page) -> None:
    """
    Ověří funkčnost navigace na stránku 'Shop'.
    Klikne na odkaz 'Shop' a zkontroluje,
    že v URL se nachází řetězec 'shop'.

    Args:
        page (Page): Otevřená stránka.
    """
    page.locator(SHOP_LINK_SELECTOR).click()
    assert "shop" in page.url.lower()


@pytest.mark.parametrize("search_term", ["serum", "ampoule", "seram"])

def test_search_functionality(page: Page, search_term: str) -> None:
    """
    Ověří funkčnost vyhledávání:
    - klikne na ikonu hledání
    - zadá parametrizovaný výraz (search_term)
    - odešle Enter
    - ověří, že výsledky obsahují hledaný text

    Args:
        page (Page): Otevřená stránka.
        search_term (str): Hledaný výraz pro test.
    """
    page.locator(SEARCH_ICON_SELECTOR).click()
    search_input = page.locator(SEARCH_INPUT_SELECTOR)
    search_input.fill(search_term)
    search_input.press("Enter")

    page.wait_for_selector(SEARCH_RESULTS_SELECTOR)
    heading_text = page.locator(SEARCH_RESULTS_SELECTOR).first.inner_text().lower()

    assert search_term in page.url.lower(), f"URL neobsahuje '{search_term}': {page.url}"
    assert search_term in heading_text, f"Nadpis výsledků neobsahuje '{search_term}': {heading_text}"
