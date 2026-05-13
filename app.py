import streamlit as st
import requests

st.set_page_config(page_title="SZEPT - TEST", layout="centered")

# --- TESTOWE WEJŚCIE NA KLUCZ ---
st.title("SZEPT - DIAGNOSTYKA")
manual_key = st.text_input("Wklej tutaj swój klucz API (AIza...)", type="password")

def test_call(key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": "Powiedz jedno słowo: TEST"}]}]}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            return "SUKCES: Połączenie działa!"
        else:
            return f"BŁĄD API: {r.status_code} - {r.text}"
    except Exception as e:
        return f"BŁĄD POŁĄCZENIA: {str(e)}"

if manual_key:
    status = test_call(manual_key)
    if "SUKCES" in status:
        st.success(status)
        st.info("Klucz jest poprawny. Jeśli SZEPT nie działa, problem leży w ustawieniach Streamlit Secrets.")
    else:
        st.error(status)

st.markdown("---")
st.write("Twoje ustawienia Secrets (czy widzę klucz?):")
if "GEMINI_KEY" in st.secrets:
    st.write("✅ Klucz GEMINI_KEY jest widoczny w Secrets")
else:
    st.write("❌ Klucz GEMINI_KEY jest NIEWIDOCZNY")
