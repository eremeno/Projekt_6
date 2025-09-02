"""Projekt: Tři automatizované testy"""

import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

URL = "https://catkoreabeauty.de/"

@pytest.fixture(scope="session")
def browser() -> Browser:
    """
    Fixture pro spuštění instance Chromium browseru.
    Browser se spustí v režimu `headless=False` s nastaveným zpomalením akcí.
    Vrací instanci browseru pro použití v testech.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    """
    Fixture pro vytvoření nové stránky (Page) v rámci testovacího kontextu.
    Otevře domovskou stránku URL a pokud se zobrazí cookie lišta,
    klikne na tlačítko pro přijetí cookies.

    Args:
        browser (Browser): Spuštěný Chromium browser.

    Returns:
        Page: Objekt stránky, se kterou testy pracují.
    """
    context: BrowserContext = browser.new_context()
    page: Page = context.new_page()
    page.goto(URL)

    cookie_btn = page.locator("button:has-text('Accept all')")
    if cookie_btn.is_visible():
        cookie_btn.click()
    yield page
    context.close()


def test_homepage_title(page: Page) -> None:
    """
    Ověří, že domovská stránka má v titulku text "Catkoreabeauty".

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
    page.locator("#menu-item-27193 > a > span").click()
    assert "shop" in page.url.lower()


def test_search_functionality(page: Page) -> None:
    """
    Ověří funkčnost vyhledávání na webu.
    Klikne na ikonu hledání, zadá výraz 'serum' a odešle Enter.
    Poté zkontroluje, že v URL se objeví řetězec 'serum'
    nebo že se zobrazí výsledky hledání.

    Args:
        page (Page): Otevřená stránka.
    """
    search_icon = page.locator("div.wd-header-search a")
    search_icon.click()
    search_input = page.locator("input.s.wd-search-inited")
    search_input.fill("serum")
    search_input.press("Enter")
    assert "serum" in page.url.lower() or page.locator("h1").first.is_visible()