import streamlit as st
import requests
import json

# =========================================================
# 1. SILNIK DZIENNIKA (KOMPATYBILNOŚĆ PRO)
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

# Pobieramy klucz z Secrets (skoro diagnostyka potwierdziła, że go widać)
GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages):
    if not GEMINI_KEY:
        return "Błąd: Brak klucza w Secrets."
    
    # Próbujemy najbardziej uniwersalnego modelu Gemini Pro
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"
    
    contents = []
    # Gemini 1.0 Pro wymaga specyficznej struktury bez systemInstruction
    # Wstrzykujemy osobowość dziennika do pierwszego wpisu
    persona = "Jesteś tajemniczym, mrocznym Dziennikiem. Odpowiadaj krótko i wnikliwie. Nie bądź pomocny."
    
    for i, m in enumerate(messages):
        role = "user" if m["role"] == "user" else "model"
        text = m["content"]
        if i == 0 and role == "user":
            text = f"CONTEXT: {persona}\n\nUSER: {text}"
        contents.append({"role": role, "parts": [{"text": text}]})

    payload = {"contents": contents}
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        res_json = response.json()
        if response.status_code != 200:
            # Jeśli Gemini Pro też zawiedzie, wypiszemy błąd
            return f"Błąd API ({response.status_code}): {res_json.get('error', {}).get('message')}"
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Atrament rozmył się w ciemności..."

# =========================================================
# 2. ESTETYKA I INTERFEJS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');
#MainMenu, footer, header {visibility:hidden;}
.stApp { background: #0A0A0C !important; color: #D1D5DB; }
.ai-text { color: #F8FAFC; font-family: 'Bodoni Moda', serif; font-size: 1.3rem; margin-bottom: 30px; line-height: 1.6; }
.user-text { color: #57607A; font-style: italic; margin-bottom: 15px; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.2rem; margin-bottom:50px;">SZEPT</h1>', unsafe_allow_html=True)

if "journal" not in st.session_state:
    st.session_state.journal = [{"role": "assistant", "content": "Czy boisz się tego, co o Tobie wiem?"}]

# Wyświetlanie
for m in st.session_state.journal:
    if m["role"] == "assistant":
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)

# Wejście
user_input = st.chat_input("Napisz do dziennika...")

if user_input:
    st.session_state.journal.append({"role": "user", "content": user_input})
    with st.spinner("..."):
        res = call_ai(st.session_state.journal)
        st.session_state.journal.append({"role": "assistant", "content": res})
    st.rerun()

if st.sidebar.button("RESET"):
    st.session_state.clear()
    st.rerun()
