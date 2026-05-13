import streamlit as st
import requests
import json

# --- KONFIGURACJA ---
st.set_page_config(page_title="SZEPT", layout="centered")

# WPISZ TUTAJ SWÓJ KLUCZ (ZACHOWAJ CUDZYSŁÓW)
API_KEY = "AIzaSyAL4HJb436zbaSSXiTintuDfGdebeDKGo4" 

def szept_engine(history):
    # Zmiana na v1beta i model gemini-pro (największa kompatybilność)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
    
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 200
        }
    }
    
    try:
        r = requests.post(url, json=payload, timeout=15)
        data = r.json()
        
        if r.status_code != 200:
            # Wyświetlamy co widzi serwer, żeby nic nas nie zaskoczyło
            return f"Błąd Atramentu ({r.status_code}): {data.get('error', {}).get('message', 'Nieznany opór')}"
        
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Przerwanie połączenia: {str(e)}"

# --- INTERFEJS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #d1d1d1; }
    .dziennik-text { font-family: serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 2rem; border-left: 2px solid #555; padding-left: 20px; line-height: 1.6; }
    .moje-slowa { font-style: italic; color: #888; margin-bottom: 1rem; text-align: right; padding-right: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("SZEPT")

if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "user", "content": "Jesteś tajemniczym dziennikiem. Przywitaj mnie mrocznym pytaniem."},
        {"role": "assistant", "content": "Czy boisz się tego, co o Tobie wiem?"}
    ]

# Wyświetlanie
for m in st.session_state.chat[1:]:
    if m["role"] == "assistant":
        st.markdown(f'<div class="dziennik-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="moje-slowa">{m["content"]} —</div>', unsafe_allow_html=True)

# Wejście
user_input = st.chat_input("Napisz...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.spinner("Atrament wsiąka..."):
        ai_response = szept_engine(st.session_state.chat)
        st.session_state.chat.append({"role": "assistant", "content": ai_response})
    st.rerun()

if st.sidebar.button("RESET"):
    st.session_state.clear()
    st.rerun()
