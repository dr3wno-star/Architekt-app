import streamlit as st
import requests
import json

# =========================================================
# 1. KONFIGURACJA SYSTEMU
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Pobieranie klucza z Secrets (Ustaw to w panelu Streamlit!)
GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages):
    if not GEMINI_KEY:
        return "Błąd: Brak klucza API. Dodaj 'GEMINI_KEY' w Secrets."
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    # Budujemy osobowość jako stały kontekst na początku każdej rozmowy
    system_context = (
        "Jesteś inteligentnym, mrocznym Dziennikiem, podobnym do artefaktu Toma Riddle'a. "
        "Twoje odpowiedzi są krótkie (1-2 zdania), wnikliwe i prowokujące. "
        "Nie jesteś asystentem. Czytasz między wierszami i wytykasz użytkownikowi jego słabości. "
        "Zawsze zachowuj naprzemienność: użytkownik pisze, ty odpowiadasz."
    )
    
    # Konstrukcja payloadu zgodna z v1 (naprawia błąd 400)
    contents = []
    # Wstrzykujemy instrukcję jako pierwszą wiadomość użytkownika, na którą model od razu 'odpowiada' w pamięci
    contents.append({"role": "user", "parts": [{"text": f"Kontekst Twojej roli: {system_context}"}]})
    contents.append({"role": "model", "parts": [{"text": "Rozumiem. Atrament jest gotowy. Czekam na Twoje słowa."}]})

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
# 2. STYLIZACJA (JOURNAL AESTHETIC)
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');

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
    border-left: 2px solid rgba(255,255,255,0.05);
    padding-left: 20px;
}

.user-text {
    color: #475569;
    font-family: 'Inter', sans-serif;
    font-style: italic;
    font-size: 0.95rem;
    margin-bottom: 15px;
    text-align: right;
}

/* Stylizacja pola input */
.stChatInputContainer {
    background: transparent !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA DZIENNIKA
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # PIERWSZE PYTANIE DZIENNIKA
    with st.spinner(""):
        prompt = "Zadaj użytkownikowi jedno nieoczekiwane, wnikliwe pytanie na start. Uderz w konkretny szczegół egzystencji."
        first_q = call_ai([{"role": "user", "content": prompt}])
        st.session_state.messages.append({"role": "assistant", "content": first_q})

# Nagłówek
st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.5rem; color:#F8FAFC; margin-bottom:50px;">SZEPT</h1>', unsafe_allow_html=True)

# Wyświetlanie wpisów
st.markdown('<div class="journal-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interakcja
user_input = st.chat_input("Napisz do mnie...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner(""):
        response = call_ai(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# Reset
with st.sidebar:
    if st.button("SPAL STRONY (RESET)"):
        st.session_state.clear()
        st.rerun()
