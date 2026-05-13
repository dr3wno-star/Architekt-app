import streamlit as st
import requests
import json

# =========================================================
# 1. KONFIGURACJA SYSTEMU I API
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Pobieranie klucza i czyszczenie go ze spacji/cytatów
raw_key = st.secrets.get("GEMINI_KEY", "")
GEMINI_KEY = raw_key.strip().replace('"', '').replace("'", "")

def call_ai(messages):
    if not GEMINI_KEY:
        return "Błąd: Brak klucza API."
    
    # Używamy wersji v1 - najbardziej stabilnej na świecie
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    # Budujemy historię rozmowy
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 1.0,
            "maxOutputTokens": 150
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=25)
        res_json = response.json()
        
        if response.status_code != 200:
            return f"Atrament zastyga... (Błąd {response.status_code})"
            
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return "Atrament rozmył się w ciemności..."

# =========================================================
# 2. INTERFEJS I STYLIZACJA
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;300;400&display=swap');

#MainMenu, footer, header {visibility:hidden;}

.stApp {
    background: #0A0A0C !important;
    color: #D1D5DB;
}

.journal-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}

.ai-text {
    color: #F8FAFC;
    font-family: 'Bodoni Moda', serif;
    font-size: 1.4rem;
    line-height: 1.6;
    margin-bottom: 45px;
}

.user-text {
    color: #475569;
    font-family: 'Inter', sans-serif;
    font-style: italic;
    font-size: 0.95rem;
    margin-bottom: 15px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    padding-bottom: 5px;
    text-align: right;
}

/* Ukrycie labela chat inputu */
.stChatInputContainer label { display: none; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA DZIENNIKA
# =========================================================

# Instrukcja osobowości wpleciona w historię
PERSONALITY_PROMPT = """Jesteś tajemniczym, inteligentnym Dziennikiem. 
Twoje odpowiedzi są krótkie (max 2 zdania), mroczne i wnikliwe. 
Nie jesteś asystentem. Czytasz między wierszami. 
Właśnie otworzyłem Twoje strony. Zadaj mi jedno nieoczekiwane pytanie, które uderzy w konkretny szczegół mojego życia lub myśli."""

if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # PIERWSZY RUCH DZIENNIKA
    with st.spinner(""):
        # Symulujemy, że użytkownik "otworzył dziennik", a AI odpowiada zgodnie z rolą
        first_q = call_ai([{"role": "user", "content": PERSONALITY_PROMPT}])
        st.session_state.messages.append({"role": "assistant", "content": first_q})

# Nagłówek
st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.5rem; color:#F8FAFC; margin-bottom:0;">SZEPT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#1E293B; letter-spacing:0.5rem; font-size:0.7rem; margin-bottom:50px;">INTERAKTYWNY ARTEFAKT</p>', unsafe_allow_html=True)

# Wyświetlanie rozmowy
st.markdown('<div class="journal-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
    elif m["content"] != PERSONALITY_PROMPT: # Nie pokazujemy promptu startowego
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Wejście użytkownika
user_input = st.chat_input("Napisz coś...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner(""):
        # Przekazujemy instrukcję na początku każdego kontekstu, by AI nie "zapomniało" kim jest
        full_context = [{"role": "user", "content": f"Pamiętaj: {PERSONALITY_PROMPT}"}] + st.session_state.messages
        response = call_ai(full_context)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# Reset
with st.sidebar:
    if st.button("SPAL STRONY (RESET)"):
        st.session_state.clear()
        st.rerun()
