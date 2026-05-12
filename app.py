import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
API_KEY = "AIzaSyBl0o-YNjRcjGeu3E362FRtPFkVIaSesjs"
genai.configure(api_key=API_KEY)

# Charakterystyka Architekta
SYSTEM_PROMPT = "Jesteś Architektem - chłodnym, inteligentnym botem elitarnej aplikacji. Badaj rozmówcę. Bądź konkretny, nie używaj emotek. Rozmawiaj po polsku."

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Wygląd
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid #C5A059; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE ARCHITECT")

# --- 2. LOGIKA AI (Zabezpieczona) ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Cześć. Nie lubię tracić czasu. Powiedz mi, co sprawia, że jesteś ciekawszy od innych?"}]

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obsługa wejścia
if prompt := st.chat_input("Napisz coś..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            # PRÓBA NR 1: Gemini 1.5 Flash (Najszybszy)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Łączymy prompt systemowy z wiadomością użytkownika w jeden strzał
            full_prompt = f"{SYSTEM_PROMPT}\n\nUżytkownik mówi: {prompt}"
            response = model.generate_content(full_prompt)
            
            res_text = response.text
            
        except Exception as e:
            # PRÓBA NR 2: Jeśli Flash zawiedzie, uderzamy w Gemini Pro (Stabilny)
            try:
                model = genai.GenerativeModel('gemini-pro')
                full_prompt = f"{SYSTEM_PROMPT}\n\nUżytkownik mówi: {prompt}"
                response = model.generate_content(full_prompt)
                res_text = response.text
            except Exception as e2:
                res_text = f"Błąd systemowy: Serwer AI odrzucił połączenie. (Kod: {str(e2)})"

        # Efekt pisania
        full_res = ""
        for chunk in res_text.split():
            full_res += chunk + " "
            placeholder.write(full_res + "▌")
            time.sleep(0.04)
        placeholder.write(full_res)
        st.session_state.messages.append({"role": "assistant", "content": res_text})
        
