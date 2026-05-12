import streamlit as st
import random
import time

# Konfiguracja stylu
st.set_page_config(page_title="The Architect", page_icon="🏛️")

st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(197, 160, 89, 0.2); }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Cześć. Nie lubię tracić czasu na uprzejmości. Powiedz mi po prostu: po co tu jesteś?"}]

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Logika dynamicznego reagowania
def get_dynamic_response(user_input):
    ui = user_input.lower()
    
    # 1. Reakcja na krótkie odpowiedzi (Siema, ok, itp)
    if len(ui.split()) < 3:
        responses = [
            "Oszczędnie. Czy w życiu też robisz tylko absolutne minimum?",
            "Mało konkretów. Boisz się, że powiem Ci o Tobie coś, czego nie chcesz usłyszeć?",
            "Siema. Ale przejdźmy do rzeczy - co Cię tu sprowadza?"
        ]
        return random.choice(responses)

    # 2. Reakcja na ambicje (dom, pieniądze, rodzina)
    if any(word in ui for word in ["dom", "rodzina", "buduj", "pieniadze", "sukces"]):
        return "Budowanie fundamentów... to brzmi jak plan. Większość tu tylko marzy, a Ty wyglądasz na kogoś, kto działa. Co jest najtrudniejsze w Twoim projekcie?"

    # 3. Reakcja na toksyczność (trolle)
    if any(word in ui for word in ["dupa", "cycki", "kurwa", "nuda"]):
        return "Tania prowokacja. Myślisz, że to wystarczy, żeby mnie zainteresować? Spróbuj jeszcze raz, tym razem z sensem."

    # 4. Uniwersalna odpowiedź "inteligentna"
    return "Ciekawy punkt widzenia. To rzadkie spotkać kogoś, kto nie mówi wyuczonymi regułkami. Co byś zrobił, gdybyś wiedział, że nie możesz zawieść?"

# Interfejs użytkownika
if prompt := st.chat_input("Napisz coś..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = get_dynamic_response(prompt)
        # Efekt pisania na żywo
        placeholder = st.empty()
        full_res = ""
        for char in response:
            full_res += char
            placeholder.write(full_res + "▌")
            time.sleep(0.02)
        placeholder.write(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
        
