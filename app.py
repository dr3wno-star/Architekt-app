import streamlit as st
import requests
import json

# --- KONFIGURACJA ---
st.set_page_config(page_title="SZEPT", layout="centered")

# RADYKALNY KROK: Wklej swój nowy klucz API między cudzysłów poniżej:
# To wykluczy błędy Streamlit Secrets.
API_KEY = "TWOJ_KLUCZ_AIZA_TUTAJ" 

def szept_engine(history):
    # Używamy najbardziej stabilnego punktu końcowego v1
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # Budujemy paczkę danych ręcznie, by uniknąć błędów JSON
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
            "maxOutputTokens": 150
        }
    }
    
    try:
        r = requests.post(url, json=payload, timeout=15)
        data = r.json()
        
        # Diagnostyka błędów wewnątrz atramentu
        if r.status_code != 200:
            return f"Błąd Atramentu: {data.get('error', {}).get('message', 'Nieznany opór')}"
        
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Przerwanie połączenia: {str(e)}"

# --- INTERFEJS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #d1d1d1; }
    .dziennik-text { font-family: serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 2rem; border-left: 2px solid #333; padding-left: 20px; }
    .moje-slowa { font-style: italic; color: #666; margin-bottom: 1rem; text-align: right; }
</style>
""", unsafe_allow_html=True)

st.title("SZEPT")

if "chat" not in st.session_state:
    # Persona wstrzyknięta jako ukryty start rozmowy
    st.session_state.chat = [
        {"role": "user", "content": "Jesteś tajemniczym dziennikiem. Przywitaj mnie mrocznym pytaniem."},
        {"role": "assistant", "content": "Czy boisz się tego, co o Tobie wiem?"}
    ]

# Wyświetlanie (omijamy pierwszy ukryty prompt instrukcyjny)
for m in st.session_state.chat[1:]:
    if m["role"] == "assistant":
        st.markdown(f'<div class="dziennik-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="moje-slowa">{m["content"]} —</div>', unsafe_allow_html=True)

# Wejście
prompt = st.chat_input("Napisz...")

if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.spinner("Wsiąkanie..."):
        odpowiedz = szept_engine(st.session_state.chat)
        st.session_state.chat.append({"role": "assistant", "content": odpowiedź})
    st.rerun()

if st.sidebar.button("SPAL DZIENNIK"):
    st.session_state.clear()
    st.rerun()
