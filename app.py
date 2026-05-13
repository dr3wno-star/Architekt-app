import streamlit as st
import requests
import json

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    contents = [{"role": "user" if m["role"] == "user" else "model", 
                 "parts": [{"text": m["content"]}]} for m in messages]

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": "Jesteś tajemniczym, mrocznym Dziennikiem. Odpowiadasz krótko (1-2 zdania). Nie jesteś pomocny – jesteś wnikliwy i prowokujący. Czytasz między wierszami i wytykasz użytkownikowi jego wahania."}]
        },
        "generationConfig": {"temperature": 1.0, "maxOutputTokens": 150}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        res_json = response.json()
        if response.status_code != 200:
            return f"Błąd API ({response.status_code}): {res_json.get('error', {}).get('message')}"
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Atrament rozmył się w ciemności..."

# ESTETYKA
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

for m in st.session_state.journal:
    role = "user-text" if m["role"] == "user" else "ai-text"
    prefix = " — " if m["role"] == "user" else ""
    st.markdown(f'<div class="{role}">{prefix}{m["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Napisz do dziennika...")

if user_input:
    st.session_state.journal.append({"role": "user", "content": user_input})
    with st.spinner("..."):
        res = call_ai(st.session_state.journal)
        st.session_state.journal.append({"role": "assistant", "content": res})
    st.rerun()

if st.sidebar.button("SPAL STRONY"):
    st.session_state.clear()
    st.rerun()
