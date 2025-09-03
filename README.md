# 🗂️Projekt: Tři automatizované testy

# Automatizované testy pro [catkoreabeauty.de](https://catkoreabeauty.de/)

Tento projekt obsahuje sadu **automatizovaných testů** vytvořených pomocí [Playwright](https://playwright.dev/python/) a [pytest](https://docs.pytest.org/).  
Testy ověřují základní funkčnost e-shopu **Cat Korea Beauty**, 
- načtení titulku domovské stránky
- funkčnost navigace na stránku **Shop**
- vyhledávání produktů (parametrizované pro více výrazů) a správná práce s cookie lištou.


## ⚙️ Použité technologie

- **Python 3.12+**
- **pytest** – testovací framework
- **Playwright (Python sync API)** – nástroj pro UI automatizaci
- **Chromium** – testovaný prohlížeč
---

## 🚀 Instalace a spuštění

### 1. Vytvoř virtuální prostředí
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 2. Nainstaluj závislosti
```bash
pip install -r requirements.txt
```

### 3. Nainstaluj Playwright prohlížeče
```bash
playwright install
```

### 4. V CI (headless režim, bez zpomalení)
```bash
HEADLESS=true SLOW_MO=0 pytest -v
```
**HEADLESS=true** → běží bez UI (vhodné pro CI/CD)

**SLOW_MO=0** → bez zpomalování kroků

## 5. Spuštění testů
```bash
pytest -v
```

### ✅ Implementované testy
1. **test_homepage_title** - Ověřuje, že domovská stránka má v titulku text Catkoreabeauty.

2. **test_navigation_to_shop** - Klikne na odkaz Shop a zkontroluje, že URL obsahuje shop.

3. **test_search_functionality** - 

- klikne na ikonu hledání

- zadá výraz (např.: serum, ampoule, milk).

- Ověří, že se hledaný výraz objeví v URL i v nadpisu výsledků.

### ⚙️ Údržba

- Selektory jsou uloženy v konstantách v horní části souboru, aby se daly snadno spravovat.

- **headless** a **slow_mo** jsou parametrizované přes proměnné prostředí → snadné použití v CI.

- **Cookie banner** má explicitní čekání (wait_for_selector) pro stabilní běh testů.

### Ukázkový výstup: 

test_catkoreabeauty.py::test_homepage_title PASSED

test_catkoreabeauty.py::test_navigation_to_shop PASSED

test_catkoreabeauty.py::test_search_functionality[serum] PASSED

test_catkoreabeauty.py::test_search_functionality[ampoule] PASSED

test_catkoreabeauty.py::test_search_functionality[milk]  PASSED

## 📚 Autor
Tento projekt byl vytvořen jako součást výukového kurzu Python Akademie od Engeto.
