import streamlit as st
import pandas as pd
import json
from openai import OpenAI
from tavily import TavilyClient
import io
from datetime import datetime, timedelta


# --- CONFIGURATION ---
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

APP_PASSWORD = "demo123"

st.set_page_config(page_title="Upsell Master | 30-Day Strategy", layout="wide")
pwd = st.sidebar.text_input("Password", type="password")

if APP_PASSWORD and pwd != APP_PASSWORD:
    st.warning("Enter demo password")
    st.stop()

# --- PRESENTATION COMPONENT ---
def render_presentation():
    # Inicjalizacja stanu slajdów
    if 'slide_index' not in st.session_state:
        st.session_state.slide_index = 0

    # Definicja slajdów (Tytuł, Opis, Plik)
    slides = [
        {
            "title": "Krok 1: Konfiguracja Celu",
            "desc": "Podaj URL hotelu i datę startu. System automatycznie zidentyfikuje lokalizację.",
            "img": "slide1.jpg"
        },
        {
            "title": "Krok 2: Analiza i Strategia 30-dniowa",
            "desc": "AI analizuje wydarzenia w okolicy (koncerty, pogoda) i tworzy kalendarz przychodów.",
            "img": "slide2.jpg"
        },
        {
            "title": "Krok 3: Szczegółowe Karty Upsellowe",
            "desc": "Każdy dzień otrzymuje 3 dedykowane oferty z opisem, ceną i wizualizacją dobraną przez AI.",
            "img": "slide3.jpg"
        },
        {
            "title": "Krok 4: Eksport Danych",
            "desc": "Gotowy plan działania z cenami i scoringiem możesz pobrać do Excela jednym kliknięciem.",
            "img": "slide4.jpg"
        }
    ]

    # UI Prezentacji w Expanderze
    with st.expander("📖 Jak działa Upsell Master? (Zobacz Prezentację)", expanded=True):
        st.markdown("### 🚀 Przewodnik po aplikacji")
        
        # Nawigacja (Strzałki i Postęp)
        col_prev, col_info, col_next = st.columns([1, 8, 1])
        
        with col_prev:
            if st.button("⬅️", key="prev"):
                if st.session_state.slide_index > 0:
                    st.session_state.slide_index -= 1
        
        with col_next:
            if st.button("➡️", key="next"):
                if st.session_state.slide_index < len(slides) - 1:
                    st.session_state.slide_index += 1
        
        # Wyświetlanie aktualnego slajdu
        curr = slides[st.session_state.slide_index]
        
        # Pasek postępu
        st.progress((st.session_state.slide_index + 1) / len(slides))
        
        st.markdown(f"#### {curr['title']}")
        st.caption(curr['desc'])
        
        # Wyświetlanie obrazka (z obsługą błędu, gdyby pliku nie było)
        try:
            st.image(curr['img'], use_container_width=True)
        except Exception:
            st.warning(f"⚠️ Brakuje pliku: {curr['img']}. Wgraj go do folderu projektu.")

# --- KONIEC KOMPONENTU ---


# --- CUSTOM STYLING ---
st.markdown("""
   <style>
   .main { background-color: #f8f9fa; }
   .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
   .upsell-card { border: 1px solid #e0e0e0; padding: 15px; border-radius: 12px; background: white; margin-bottom: 20px; }
   </style>
   """, unsafe_allow_html=True)


st.sidebar.title("🛠️ Upsell Master")
st.sidebar.markdown("Advanced Upsell Revenue Engine")


# --- ENGINE ---


def get_30_day_strategy(hotel_url, start_date):
   client = OpenAI(api_key=OPENAI_API_KEY)
   tavily = TavilyClient(api_key=TAVILY_API_KEY)
  
   with st.status("🛸 Upsell Master is analyzing the next 30 days...", expanded=True):
       # Step 1: Broad Research for the month
       st.write("Scanning local events, holidays, and market trends...")
       search_query = f"Major events, concerts, festivals and holidays in the city of hotel {hotel_url} from {start_date} for the next 30 days"
       context_data = tavily.search(query=search_query, search_depth="advanced")


       # Step 2: AI Generation (Full 30-day roadmap)
       st.write("Generating personalized upsell offers using GPT")
      
       system_msg = """You are 'Upsell Master', a world-class Revenue Manager.
       Your goal is to maximize hotel profit by matching upsells to specific calendar dates.
       Return ONLY a JSON object with a key 'calendar' containing a list of 30 days.
       Each day must have:
       - date: (YYYY-MM-DD)
       - event_context: (What's happening?)
       - top_3_upsells: List of 3 objects {name, description, price (NUMBER ONLY), score (1-10), image_keyword (ONE WORD)}
       - other_recommendations: List of 2 secondary service names.
       """
      
       user_msg = f"Hotel URL: {hotel_url}. Start Date: {start_date}. Context: {context_data}"
      
       response = client.chat.completions.create(
           model="gpt-5.2", # Używamy najsilniejszego modelu
           response_format={"type": "json_object"},
           messages=[
               {"role": "system", "content": system_msg},
               {"role": "user", "content": user_msg}
           ]
       )
      
       return json.loads(response.choices[0].message.content)['calendar']


# --- UI ---


st.title("📅 30-Day Revenue Roadmap")
render_presentation()
hotel_url = st.text_input("Hotel URL", "https://citysoleil.pl/")
start_date = st.date_input("Strategy Start Date", datetime.now())


if st.button("Generate 30-Day Master Plan"):
   strategy = get_30_day_strategy(hotel_url, str(start_date))
  
   # Pre-process for Table
   table_data = []
   for day in strategy:
       top_1 = day['top_3_upsells'][0]
       table_data.append({
           "Date": day['date'],
           "Local Context": day['event_context'],
           "Best Upsell": top_1['name'],
           "Price": f"{top_1['price']} PLN",
           "AI Score": top_1['score']
       })
  
   df = pd.DataFrame(table_data)
  
   # 1. Summary Table
   st.subheader("📊 Monthly Overview")
   st.dataframe(df, use_container_width=True)
  
   # 2. Daily Deep Dive
   st.divider()
   st.subheader("🔍 Detailed Daily Insights")
  
   # Selektor dnia do podglądu kart
   selected_day_str = st.selectbox("Select a day to view detailed cards:", [d['date'] for d in strategy])
   day_data = next(item for item in strategy if item["date"] == selected_day_str)
  
   st.info(f"**Event Context:** {day_data['event_context']}")
  
   cols = st.columns(3)
   for i, upsell in enumerate(day_data['top_3_upsells']):
       with cols[i]:
           # Poprawione dobieranie obrazka
           keyword = upsell['image_keyword']
           img_url = f"https://loremflickr.com/400/300/hotel,{keyword}?lock={i}"
          
           st.image(img_url, use_container_width=True)
           st.markdown(f"### {upsell['name']}")
           st.write(upsell['description'])
           st.metric("Price", f"{upsell['price']} PLN")
           st.progress(upsell['score'] / 10, text=f"Match Score: {upsell['score']}/10")
          
   st.markdown(f"**Other opportunities for this day:** {', '.join(day_data['other_recommendations'])}")


   # 3. Export
   st.divider()
   output = io.BytesIO()
   with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
       full_export_data = []
       for day in strategy:
           for u in day['top_3_upsells']:
               full_export_data.append({
                   "Date": day['date'],
                   "Event": day['event_context'],
                   "Upsell": u['name'],
                   "Price": u['price'],
                   "Score": u['score']
               })
       pd.DataFrame(full_export_data).to_excel(writer, index=False)
  
   st.download_button("📥 Download Full 30-Day Excel Report", output.getvalue(), "upsell_master_plan.xlsx")
