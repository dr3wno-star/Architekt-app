import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
# Wklej swój klucz API poniżej
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

# Używamy modelu Flash, który ma wysokie limity darmowe
MODEL_NAME = 'models/gemini-1.5-flash'

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Stylizacja
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03); border-radius: 10px; border-left: 3px solid #C5A059; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKA CZATU ---
SYSTEM_PROMPT = "Jesteś Architektem. Chłodny, elitarny ton. Selekcja randkowa. Mów krótko po polsku."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System aktywny. Czego oczekujesz od elity?"}]

st.title("🏛️ THE ARCHITECT")

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obsługa wejścia
if prompt := st.chat_input("Twoja odpowiedź..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            # Tworzymy model
            model = genai.GenerativeModel(MODEL_NAME)
            
            # Budujemy zapytanie
            full_query = f"{SYSTEM_PROMPT}\nUżytkownik: {prompt}\nArchitekt:"
            
            # Generujemy odpowiedź
            response = model.generate_content(full_query)
            res_text = response.text
            
            # Efekt pisania
            full_res = ""
            for chunk in res_text.split():
                full_res += chunk + " "
                placeholder.write(full_res + "▌")
                time.sleep(0.05)
            placeholder.write(full_res)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"Błąd systemu: {str(e)}")
            
