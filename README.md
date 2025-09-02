# 🗂️Projekt: Tři automatizované testy

# Automatizované testy pro [catkoreabeauty.de](https://catkoreabeauty.de/)

Tento projekt obsahuje sadu **automatizovaných testů** vytvořených pomocí [Playwright](https://playwright.dev/python/) a [pytest](https://docs.pytest.org/).  
Testy ověřují základní funkčnost e-shopu **Cat Korea Beauty**, jako je načtení domovské stránky,  
navigace do obchodu, vyhledávání produktů a správná práce s cookie lištou.


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

## 🧪 Spuštění testů

### Spuštění všech testů:
```bash
pytest -v
```

### ✅ Implementované testy
1. **test_homepage_title** - Ověřuje, že domovská stránka má v titulku text Catkoreabeauty.

2. **test_navigation_to_shop** - Klikne na odkaz Shop a zkontroluje, že URL obsahuje shop.

3. **test_search_functionality** - Ověří funkčnost vyhledávání: zadá serum a ověří, že výsledky odpovídají.

### 🔒 Cookie lišta

Testy automaticky detekují a přijímají cookies kliknutím na tlačítko
**„Accept all“**, pokud se cookie lišta zobrazí.

## 📚 Autor
Tento projekt byl vytvořen jako součást výukového kurzu Python Akademie od Engeto.
