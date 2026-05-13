import streamlit as st
import google.generativeai as genai

# --- KONFIGURACJA ---
st.set_page_config(page_title="SZEPT", layout="centered")

# WPISZ TUTAJ SWÓJ KLUCZ (ZACHOWAJ CUDZYSŁÓW)
API_KEY = "AIzaSyDCmJ-nxrYU3w1MSzPNij5KYd6r1Btfbog" 

# Inicjalizacja modelu za pomocą oficjalnej biblioteki
try:
    genai.configure(api_key=API_KEY)
    # Używamy modelu bez wersji w nazwie, by biblioteka sama go znalazła
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Błąd konfiguracji: {e}")

def szept_engine(history):
    try:
        # Konwersja formatu rozmowy dla biblioteki Google
        chat = model.start_chat(history=[])
        # Wysyłamy ostatnią wiadomość użytkownika z kontekstem mrocznego dziennika
        persona = "Jesteś mrocznym, tajemniczym dziennikiem. Odpowiadaj krótko i niepokojąco."
        full_prompt = f"{persona}\n\nUżytkownik mówi: {history[-1]['content']}"
        
        response = chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        return f"Atrament zastyga ({str(e)})"

# --- INTERFEJS ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #d1d1d1; }
    .dziennik-text { font-family: serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 2rem; border-left: 2px solid #555; padding-left: 20px; line-height: 1.6; }
    .moje-slowa { font-style: italic; color: #888; margin-bottom: 1rem; text-align: right; padding-right: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("SZEPT")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Czy boisz się tego, co o Tobie wiem?"}
    ]

# Wyświetlanie
for m in st.session_state.chat_history:
    if m["role"] == "assistant":
        st.markdown(f'<div class="dziennik-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="moje-slowa">{m["content"]} —</div>', unsafe_allow_html=True)

# Wejście
user_input = st.chat_input("Napisz...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Wsiąkanie..."):
        ai_response = szept_engine(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    st.rerun()

if st.sidebar.button("RESET"):
    st.session_state.clear()
    st.rerun()
