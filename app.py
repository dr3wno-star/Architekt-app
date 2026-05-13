import streamlit as st
import requests
import json

# =========================================================
# 1. KONFIGURACJA I SILNIK (NAJBARDZIEJ KOMPATYBILNY)
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages, sys_prompt):
    if not GEMINI_KEY:
        return "Błąd: Brak klucza API w Secrets."
    
    # Próbujemy najbardziej standardowy punkt końcowy
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": sys_prompt}]},
        "generationConfig": {
            "temperature": 1.0,
            "maxOutputTokens": 200
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        res_json = response.json()
        
        if response.status_code != 200:
            # Jeśli nadal 404, spróbujemy podpowiedzieć co jest nie tak
            err_msg = res_json.get('error', {}).get('message', 'Nieznany błąd')
            return f"Błąd API ({response.status_code}): {err_msg}"
            
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Błąd połączenia: {str(e)}"

# =========================================================
# 2. STYLE (DZIENNIK)
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
    
    # Próba wygenerowania pierwszego pytania
    sys_init = "Jesteś tajemniczym Dziennikiem. Zadaj krótkie, niepokojące pytanie otwierające."
    
    with st.spinner("..."):
        first_q = call_ai([{"role": "user", "content": "Zadaj mi pierwsze pytanie."}], sys_init)
        st.session_state.journal.append({"role": "assistant", "content": first_q})

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.2rem; margin-top:50px;">SZEPT</h1>', unsafe_allow_html=True)

# Wyświetlanie
st.markdown('<div class="journal-page">', unsafe_allow_html=True)
for m in st.session_state.journal:
    if m["role"] == "user":
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Wejście użytkownika
user_input = st.chat_input("Twoja odpowiedź...")

if user_input:
    st.session_state.journal.append({"role": "user", "content": user_input})
    sys_prompt = "Jesteś Dziennikiem. Odpowiadaj krótko i inteligentnie."
    
    with st.spinner("..."):
        response = call_ai(st.session_state.journal, sys_prompt)
        st.session_state.journal.append({"role": "assistant", "content": response})
    st.rerun()

if st.sidebar.button("RESET"):
    st.session_state.clear()
    st.rerun()
