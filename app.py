import streamlit as st
import google.generativeai as genai
import time

# =========================================================
# 1. KONFIGURACJA SYSTEMU (OFICJALNE SDK)
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Pobieranie klucza z Secrets
GEMINI_KEY = st.secrets.get("GEMINI_KEY")

if not GEMINI_KEY:
    st.error("Błąd: Brak klucza API w Secrets (GEMINI_KEY).")
    st.stop()

# Konfiguracja modelu
genai.configure(api_key=GEMINI_KEY)

# Definicja osobowości Dziennika
SYSTEM_INSTRUCTION = (
    "Jesteś inteligentnym, mrocznym Dziennikiem, podobnym do artefaktu Toma Riddle'a. "
    "Twoje odpowiedzi są krótkie (1-2 zdania), wnikliwe i prowokujące. "
    "Nie jesteś asystentem. Czytasz między wierszami i wytykasz użytkownikowi jego słabości. "
    "Gdy użytkownik milczy lub zaczynasz rozmowę, zadaj jedno nieoczekiwane, surowe pytanie."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

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
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA DZIENNIKA
# =========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
    # PIERWSZE PYTANIE DZIENNIKA
    with st.spinner(""):
        try:
            # Generujemy otwarcie bez historii
            response = model.generate_content("Zadaj użytkownikowi jedno nieoczekiwane, surowe pytanie na start. Uderz w konkretny szczegół egzystencji.")
            st.session_state.chat_history.append({"role": "model", "parts": [response.text]})
        except Exception as e:
            st.error(f"Atrament zastyga... (Błąd: {e})")

# Nagłówek
st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.5rem; color:#F8FAFC; margin-bottom:50px;">SZEPT</h1>', unsafe_allow_html=True)

# Wyświetlanie wpisów
st.markdown('<div class="journal-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    role = "ai" if message["role"] == "model" else "user"
    text = message["parts"][0]
    if role == "ai":
        st.markdown(f'<div class="ai-text">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-text"> — {text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interakcja
user_input = st.chat_input("Napisz do mnie...")

if user_input:
    # Dodaj wpis użytkownika do historii
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})
    
    with st.spinner(""):
        try:
            # Używamy start_chat by zachować kontekst całej rozmowy
            chat = model.start_chat(history=st.session_state.chat_history[:-1])
            response = chat.send_message(user_input)
            st.session_state.chat_history.append({"role": "model", "parts": [response.text]})
        except Exception as e:
            st.error("Atrament rozmył się w ciemności...")
    
    st.rerun()

# Reset
with st.sidebar:
    if st.button("SPAL STRONY (RESET)"):
        st.session_state.clear()
        st.rerun()
