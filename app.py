import streamlit as st
import google.generativeai as genai
import time

# 1. Konfiguracja "Mózgu"
genai.configure(api_key="AIzaSyBl0o-YNjRcjGeu3E362FRtPFkVIaSesjs")

# Instrukcja systemowa - definiuje charakter bota
SYSTEM_PROMPT = """
Jesteś 'Architektem' - inteligentnym, chłodnym, ale intrygującym botem elitarnej aplikacji. 
Twoim zadaniem jest rozmowa z użytkownikiem, aby wybadać jego status, inteligencję i intencje.
Zasady:
- Nie bądź miły na siłę. Bądź konkretny.
- Jeśli ktoś trolluje (wulgaryzmy, stopy, głupoty) - bądź sarkastyczny i chłodny.
- Jeśli ktoś pisze o celach (dom, rodzina, biznes) - okaż szacunek i drąż temat.
- Rozmawiaj po polsku.
"""

# Tworzymy model z wbudowaną instrukcją (to eliminuje błąd NotFound przy send_message)
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT
)

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Wygląd
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(197, 160, 89, 0.2); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE ARCHITECT")

# Inicjalizacja sesji czatu
if "chat_session" not in st.session_state:
    # Startujemy czat bez wysyłania SYSTEM_PROMPT jako wiadomości (to naprawia błąd)
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.messages = [{"role": "assistant", "content": "Cześć. Nie lubię tracić czasu. Powiedz mi, co sprawia, że jesteś ciekawszy od tysięcy innych ludzi w tej sieci?"}]

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obsługa czatu
if prompt := st.chat_input("Napisz coś..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # Pobieranie odpowiedzi
        try:
            response = st.session_state.chat_session.send_message(prompt)
            for chunk in response.text.split():
                full_res += chunk + " "
                placeholder.write(full_res + "▌")
                time.sleep(0.04)
            placeholder.write(full_res)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Szczegóły błędu: {e}")
            
