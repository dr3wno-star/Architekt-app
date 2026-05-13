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

# Pobieranie klucza z Secrets
GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages, sys_instruction):
    if not GEMINI_KEY:
        return "Błąd: Klucz API nie został skonfigurowany w Secrets."
    
    # Korzystamy z wersji v1beta, która najlepiej obsługuje system_instruction
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    # Mapowanie ról na format Gemini
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": sys_instruction}]
        },
        "generationConfig": {
            "temperature": 1.0,
            "maxOutputTokens": 150,
            "topP": 0.95
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
# 2. INTERFEJS I STYLIZACJA (SZEPT AESTHETIC)
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;300;400&display=swap');

/* Ukrycie elementów Streamlit */
#MainMenu, footer, header {visibility:hidden;}

/* Tło i główny kontener */
.stApp {
    background: #0A0A0C !important;
    color: #D1D5DB;
}

/* Stylizacja strony dziennika */
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
    opacity: 0;
    animation: fadeIn 2s forwards;
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

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Stylizacja inputu */
.stChatInputContainer {
    padding-bottom: 50px !important;
    background: transparent !important;
}

input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #1E293B !important;
    color: #F8FAFC !important;
    font-size: 1.1rem !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA INTERAKCJI (DZIENNIK)
# =========================================================

# Instrukcja osobowości dla AI
SYSTEM_PROMPT = """Jesteś tajemniczym, inteligentnym Dziennikiem. 
Twoim zadaniem jest interakcja z użytkownikiem, ale nie jesteś pomocnym asystentem. 
Jesteś wnikliwym obserwatorem, który czyta między wierszami. 
Twoje odpowiedzi są krótkie (max 2 zdania), mroczne, prowokujące i niezwykle trafne. 
Dostrzegaj lęk, wahanie lub pychę w słowach użytkownika. 
Gdy zaczynasz rozmowę, zadaj jedno nieoczekiwane pytanie, które uderzy w konkretny szczegół."""

# Inicjalizacja sesji
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # PIERWSZY RUCH DZIENNIKA
    with st.spinner(""):
        first_q = call_ai(
            [{"role": "user", "content": "Zbudź się i przejmij inicjatywę. Zadaj mi pierwsze pytanie."}], 
            SYSTEM_PROMPT
        )
        st.session_state.messages.append({"role": "assistant", "content": first_q})

# Nagłówek
st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.5rem; color:#F8FAFC; margin-bottom:0;">SZEPT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#1E293B; letter-spacing:0.5rem; font-size:0.7rem; margin-bottom:50px;">INTERAKTYWNY ARTEFAKT</p>', unsafe_allow_html=True)

# Wyświetlanie rozmowy
st.markdown('<div class="journal-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Wejście użytkownika (Chat Input na dole)
user_input = st.chat_input("Napisz coś, by wchłonął to atrament...")

if user_input:
    # Dodaj wpis użytkownika
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generuj odpowiedź dziennika
    with st.spinner(""):
        response = call_ai(st.session_state.messages, SYSTEM_PROMPT)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Odśwież, by pokazać nową treść
    st.rerun()

# Panel boczny tylko dla Resetu
with st.sidebar:
    st.markdown("### Zarządzanie Artefaktem")
    if st.button("SPAL STRONY (RESET)"):
        st.session_state.clear()
        st.rerun()
