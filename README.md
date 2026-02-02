# 🏨 Upsell Master AI | Intelligent Revenue Engine

**Upsell Master** to prototyp (MVP) agenta AI wspierającego managerów hoteli w maksymalizacji przychodów (Revenue Management). Aplikacja automatycznie analizuje lokalny rynek i generuje 30-dniową strategię dosprzedaży usług (upselling), dopasowaną do wydarzeń w mieście i specyfiki daty.

---

## 🚀 O Projekcie

Celem projektu jest rozwiązanie problemu statycznych ofert hotelowych. Zamiast oferować każdemu gościowi to samo, system wykorzystuje **Agentic AI** do łączenia danych zewnętrznych z logiką sprzedażową.

### Kluczowe Funkcjonalności:
* **🔍 Live Market Research:** Integracja z Tavily API do skanowania wydarzeń, koncertów i świąt w lokalizacji hotelu na 30 dni w przód.
* **🧠 AI Reasoning:** Model OpenAI analizuje kontekst (np. "Walentynki", "Koncert Rockowy") i dobiera najlepsze usługi dodatkowe (SPA, Kolacja, Transport).
* **📊 Scoring Ofert:** Każda propozycja otrzymuje ocenę dopasowania (1-10) wraz z uzasadnieniem.
* **📑 Eksport Danych:** Możliwość pobrania gotowego harmonogramu w formacie Excel (.xlsx) do dalszej obróbki.
* **🛡️ Bezpieczeństwo:** Prosty system autoryzacji hasłem.

---

## 🛠️ Stack Technologiczny

Projekt został zbudowany w oparciu o nowoczesny stack Python AI:

* **Core:** Python 3.9+
* **Frontend:** Streamlit (Szybkie prototypowanie UI)
* **AI Logic:** OpenAI API (GPT-4o/GPT-4o-mini)
* **Web Search Agent:** Tavily API (Search-as-a-service dla LLM)
* **Data Processing:** Pandas, XlsxWriter

---

## ⚙️ Instalacja i Uruchomienie

Aby uruchomić projekt lokalnie, wykonaj następujące kroki:

### 1. Sklonuj repozytorium
```bash
git clone [https://github.com/twoj-login/upsell-master.git](https://github.com/twoj-login/upsell-master.git)
cd upsell-master
