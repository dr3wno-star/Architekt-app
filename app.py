import streamlit as st
import json

st.title("SZEPT - Diagnoza Połączenia")

# Sprawdźmy co Streamlit "widzi"
st.write("### Status Sekretów:")

# Sprawdzanie Gemini
if "GEMINI_KEY" in st.secrets:
    st.success("✅ Klucz Gemini: ZNALEZIONY")
else:
    st.error("❌ Klucz Gemini: NIEZNALEZIONY (Streamlit szuka nazwy: GEMINI_KEY)")

# Sprawdzanie Firebase
if "FIREBASE_SERVICE_ACCOUNT" in st.secrets:
    st.success("✅ Firebase JSON: ZNALEZIONY")
    try:
        data = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
        st.write(f"Zalogowano do projektu: `{data.get('project_id')}`")
    except Exception as e:
        st.error(f"❌ Błąd formatu JSON w Firebase: {e}")
else:
    st.error("❌ Firebase JSON: NIEZNALEZIONY (Streamlit szuka nazwy: FIREBASE_SERVICE_ACCOUNT)")

st.write("---")
st.write("Wszystkie znalezione klucze w Secrets:", list(st.secrets.keys()))

if st.button("Odśwież diagnozę"):
    st.rerun()
    
