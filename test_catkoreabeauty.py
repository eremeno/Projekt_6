"""
Projekt: Tři automatizované testy
Popis:
Tento projekt obsahuje tři testy automatizované pomocí Playwright a pytest:
1. Ověření titulku domovské stránky.
2. Ověření funkčnosti navigace na stránku "Shop".
3. Parametrizované testy vyhledávání pro různé výrazy.
"""

import os
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

URL: str = "https://catkoreabeauty.de/"

COOKIE_BTN_SELECTOR: str = "button:has-text('Accept all')"
SHOP_LINK_SELECTOR: str = "#menu-item-27193 > a > span"
SEARCH_ICON_SELECTOR: str = "div.wd-header-search a"
SEARCH_INPUT_SELECTOR: str = "input.s.wd-search-inited"
SEARCH_RESULTS_SELECTOR: str = "h1"


@pytest.fixture(scope="session")
def browser() -> Browser:
    """
    Fixture pro spuštění instance Chromium browseru.
    Pro konfiguraci se používají environmentální proměnné:
        HEADLESS (str): "true"/"false" – určuje, zda se spustí v headless režimu.
        SLOW_MO (str): Počet milisekund zpomalení mezi akcemi (výchozí 2000 ms).

    Returns:
        Browser: Spuštěná instance Chromium browseru.
    """
    headless: bool = os.getenv("HEADLESS", "false").lower() == "true"
    slow_mo: int = int(os.getenv("SLOW_MO", "2000"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    """
    Fixture pro vytvoření nové stránky (Page).
    Otevře domovskou stránku a přijme cookies, pokud je zobrazen banner.

    Args:
        browser (Browser): Instance prohlížeče Playwright Chromium.

    Yields:
        Page: Otevřená stránka s připraveným kontextem.
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
    Test: Ověří, že domovská stránka má v titulku text 'Catkoreabeauty'.
    
    Args:
        page (Page): Otevřená stránka.
    """
    assert "Catkoreabeauty" in page.title()


def test_navigation_to_shop(page: Page) -> None:
    """
    Test: Ověří funkčnost navigace na stránku 'Shop'.
    Klikne na odkaz 'Shop' a zkontroluje,
    že v URL se nachází řetězec 'shop'.

    Args:
        page (Page): Otevřená stránka.
    """
    page.locator(SHOP_LINK_SELECTOR).click()
    assert "shop" in page.url.lower()


@pytest.mark.parametrize("search_term", ["serum", "ampoule", "milk"])

def test_search_functionality(page: Page, search_term: str) -> None:
    """
    Test: Ověří funkčnost vyhledávání na e-shopu.
    Postup:
        - klikne na ikonu hledání,
        - zadá parametrizovaný výraz (search_term),
        - odešle Enter,
        - ověří, že výsledky obsahují hledaný text
          jak v URL, tak v hlavním nadpisu.

    Args:
        page (Page): Otevřená stránka.
        search_term (str): Hledaný výraz pro test.
    """
    page.locator(SEARCH_ICON_SELECTOR).click()
    search_input = page.locator(SEARCH_INPUT_SELECTOR)
    search_input.fill(search_term)
    search_input.press("Enter")

    page.wait_for_selector(SEARCH_RESULTS_SELECTOR)
    heading_text = str =page.locator(SEARCH_RESULTS_SELECTOR).first.inner_text().lower()

    assert search_term in page.url.lower()
    assert search_term in heading_text
