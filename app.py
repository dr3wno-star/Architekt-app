import streamlit as st
import requests
import json

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

# --- PRÓBA POBRANIA KLUCZA NA 2 SPOSOBY ---
GEMINI_KEY = st.secrets.get("GEMINI_KEY", "")

# Jeśli klucza nie ma w Secrets, pozwól wpisać go ręcznie w sidebarze
if not GEMINI_KEY or len(GEMINI_KEY) < 5:
    st.sidebar.warning("Brak klucza w systemie.")
    GEMINI_KEY = st.sidebar.text_input("Wklej klucz API (AIza...)", type="password")

def call_ai(messages):
    if not GEMINI_KEY:
        return "Błąd: Brak klucza. Wklej go w panelu bocznym."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    contents = [{"role": "user" if m["role"] == "user" else "model", 
                 "parts": [{"text": m["content"]}]} for m in messages]

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": "Jesteś tajemniczym, inteligentnym Dziennikiem. Odpowiadasz krótko (1-2 zdania). Nie jesteś pomocny – jesteś wnikliwy, mroczny i prowokujący."}]
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        res_json = response.json()
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Błąd API ({response.status_code}): {res_json.get('error', {}).get('message', 'Nieprawidłowy klucz')}"
    except:
        return "Atrament zastyga..."

# --- ESTETYKA ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');
#MainMenu, footer, header {visibility:hidden;}
.stApp { background: #08080A !important; color: #D1D5DB; }
.ai-text { color: #F8FAFC; font-family: 'Bodoni Moda', serif; font-size: 1.4rem; margin-bottom: 35px; line-height: 1.6; animation: fade 2s ease-in; }
.user-text { color: #57607A; font-style: italic; margin-bottom: 20px; font-size: 0.95rem; }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.2rem; margin-top:50px;">SZEPT</h1>', unsafe_allow_html=True)

if "journal" not in st.session_state:
    st.session_state.journal = [{"role": "assistant", "content": "Czy boisz się tego, co o Tobie wiem?"}]

# Wyświetlanie rozmowy
st.markdown('<div style="margin-top:50px;">', unsafe_allow_html=True)
for m in st.session_state.journal:
    if m["role"] == "assistant":
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interakcja
user_input = st.chat_input("Napisz...")

if user_input:
    st.session_state.journal.append({"role": "user", "content": user_input})
    with st.spinner("Atrament chłonie..."):
        res = call_ai(st.session_state.journal)
        st.session_state.journal.append({"role": "assistant", "content": res})
    st.rerun()

if st.sidebar.button("RESET"):
    st.session_state.clear()
    st.rerun()
