import streamlit as st
import time

# Konfiguracja wizualna "The Architect"
st.set_page_config(page_title="The Architect", page_icon="🏛️")

st.markdown("""
    <style>
    .stApp {
        background-color: #1A1A1B;
        color: #C5A059;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(197, 160, 89, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE ARCHITECT")
st.caption("AI-Driven Human Connection")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Cześć. Nie będę Cię pytać, jak mija dzień. Powiedz mi: jesteś tu, bo faktycznie masz do zaoferowania coś więcej niż reszta?"}
    ]

# Wyświetlanie historii chatu
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Reakcja na wpis użytkownika
if prompt := st.chat_input("Twoja odpowiedź..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Logika AI "pod maską"
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Tutaj AI "myśli"
        full_response = ""
        
        # Prosta logika reakcji (do rozbudowania o LLM API)
        if any(word in prompt.lower() for word in ["siema", "hej"]):
            response = "Konkretnie. Skoro oszczędzasz słowa, to mam nadzieję, że przeznaczasz tę energię na coś ważniejszego. Co w sobie szanujesz najbardziej?"
        elif len(prompt.split()) > 5:
            response = "To, co piszesz, ma swoją wagę. Widzę, że nie boisz się wychodzić przed szereg. Budowanie czegoś trwałego wymaga takiej pewności. Co jest Twoim głównym celem?"
        else:
            response = "Rozumiem. Ale tutaj szukamy głębi. Spróbuj przekonać mnie, że warto kontynuować tę rozmowę."

        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.1)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
  
