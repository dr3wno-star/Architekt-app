import streamlit as st
import google.generativeai as genai
import time

# 1. Konfiguracja "Mózgu" (AI)
genai.configure(api_key="AIzaSyCPuOlL-SbSjQekmOyQAr0aeAu06rQqymM") # Wklej tu swój klucz!
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Instrukcja dla AI (Niewidoczna dla użytkownika)
SYSTEM_PROMPT = """
Jesteś 'Architektem' - inteligentnym, chłodnym, ale intrygującym botem elitarnej aplikacji. 
Twoim zadaniem jest rozmowa z użytkownikiem, aby wybadać jego status, inteligencję i intencje.
Zasady:
- Nie bądź miły na siłę. Bądź konkretny.
- Jeśli ktoś trolluje (pisze o stopach, wulgaryzmy) - bądź sarkastyczny i chłodny.
- Jeśli ktoś pisze o celach (dom, rodzina, biznes) - okaż szacunek i drąż temat.
- Rozmawiaj po polsku, używaj naturalnego, nowoczesnego języka.
- Nigdy nie przyznawaj, że jesteś modelem AI od Google. Jesteś Architektem.
"""

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Stylizacja wizualna
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(197, 160, 89, 0.2); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE ARCHITECT")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    # Wysyłamy instrukcję systemową na starcie (ukryte)
    st.session_state.chat_session.send_message(SYSTEM_PROMPT)
    st.session_state.messages = [{"role": "assistant", "content": "Cześć. Nie lubię tracić czasu. Powiedz mi, co sprawia, że jesteś ciekawszy od tysięcy innych ludzi w tej sieci?"}]

# Wyświetlanie rozmowy
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obsługa wpisywania
if prompt := st.chat_input("Napisz coś..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        # Pobieranie odpowiedzi od prawdziwego AI
        response = st.session_state.chat_session.send_message(prompt)
        
        for chunk in response.text.split():
            full_res += chunk + " "
            placeholder.write(full_res + "▌")
            time.sleep(0.05)
        placeholder.write(full_res)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    
