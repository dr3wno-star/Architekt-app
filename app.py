import streamlit as st
import requests
import json

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")
GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages, sys_prompt):
    # Próbujemy najstarszego i najbardziej stabilnego modelu
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"
    
    contents = []
    # Gemini 1.0 Pro nie obsługuje systemInstruction w API, wstrzykujemy to do tekstu
    full_prompt = f"SYSTEM: {sys_prompt}\n\nUSER: {messages[-1]['content']}"
    contents.append({"role": "user", "parts": [{"text": full_prompt}]})

    payload = {"contents": contents}
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        res_json = response.json()
        if response.status_code != 200:
            return f"Błąd API ({response.status_code}): {res_json.get('error', {}).get('message')}"
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Błąd: {str(e)}"

# --- PROSTY INTERFEJS ---
st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.2rem;">SZEPT</h1>', unsafe_allow_html=True)

if "journal" not in st.session_state:
    st.session_state.journal = [{"role": "assistant", "content": "Czy boisz się tego, co o Tobie wiem?"}]

for m in st.session_state.journal:
    st.write(f"**{'Dziennik' if m['role']=='assistant' else 'Ty'}:** {m['content']}")

user_input = st.chat_input("Napisz...")
if user_input:
    st.session_state.journal.append({"role": "user", "content": user_input})
    res = call_ai(st.session_state.journal, "Jesteś mrocznym dziennikiem.")
    st.session_state.journal.append({"role": "assistant", "content": res})
    st.rerun()
