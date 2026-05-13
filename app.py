import streamlit as st
import requests
import json

# =========================================================
# 1. KONFIGURACJA I SILNIK (NAPRAWA BŁĘDU 404)
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages, sys_prompt):
    if not GEMINI_KEY:
        return "Błąd: Brak klucza API w Secrets."
    
    # Zmiana na wersję v1 i pełną nazwę modelu
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    contents = []
    # Gemini v1 wymaga konkretnej struktury: role 'user' lub 'model'
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": sys_prompt}]},
        "generationConfig": {
            "temperature": 1.0,
            "maxOutputTokens": 250,
            "topP": 0.95,
            "topK": 40
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        res_json = response.json()
        
        if response.status_code != 200:
            return f"Błąd API ({response.status_code}): {res_json.get('error', {}).get('message')}"
            
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Błąd połączenia: {str(e)}"

# =========================================================
# 2. ESTETYKA
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');
#MainMenu, footer, header {visibility:hidden;}
.stApp { background: #0A0A0C !important; color: #D1D5DB; }
.journal-page { border-left: 1px solid rgba(255,255,255,0.05); padding-left: 30px; margin-top: 30px; }
.ai-text { color: #F8FAFC; font-family: 'Bodoni Moda', serif; font-size: 1.35rem; margin-bottom: 40px; line-height: 1.6; }
.user-text { color: #57607A; font-style: italic; margin-bottom: 20px; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA DZIENNIKA
# =========================================================

if "journal" not in st.session_state:
    st.session_state.journal = []
    
    # INICJACJA - DZIENNIK ZADAJE PIERWSZE PYTANIE
    sys_init = """Jesteś tajemniczym, inteligentnym Dziennikiem. 
    Zadaj jedno krótkie, przenikliwe i nieoczekiwane pytanie, które sprawi, że użytkownik poczuje Twoją obecność. 
    Nie pytaj o samopoczucie. Zapytaj o coś surowego i konkretnego."""
    
    with st.spinner("Czekaj, atrament schnie..."):
        first_q = call_ai([{"role": "user", "content": "Zadaj mi pierwsze pytanie."}], sys_init)
        st.session_state.journal.append({"role": "assistant", "content": first_q})

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.2rem; margin-top:50px;">SZEPT</h1>', unsafe_allow_html=True)

# Wyświetlanie wpisów
st.markdown('<div class="journal-page">', unsafe_allow_html=True)
for m in st.session_state.journal:
    if m["role"] == "user":
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interfejs wpisywania
user_input = st.chat_input("Twoja odpowiedź...")

if user_input:
    st.session_state.journal.append({"role": "user", "content": user_input})
    
    sys_prompt = "Jesteś Dziennikiem. Odpowiadaj krótko (1-2 zdania), prowokująco i inteligentnie. Dostrzegaj to, co ukryte między słowami użytkownika."
    
    with st.spinner("Wchłanianie..."):
        response = call_ai(st.session_state.journal, sys_prompt)
        st.session_state.journal.append({"role": "assistant", "content": response})
    st.rerun()

# Przycisk resetu na dole
st.sidebar.markdown("---")
if st.sidebar.button("SPAL STRONY (RESET)"):
    st.session_state.clear()
    st.rerun()
