import streamlit as st
import time
import random

# =========================================================
# 1. KONFIGURACJA ESTETYKI
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');

#MainMenu, footer, header {visibility:hidden;}

.stApp {
    background: #0A0A0C !important;
    color: #D1D5DB;
}

.journal-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}

.ai-text {
    color: #F8FAFC;
    font-family: 'Bodoni Moda', serif;
    font-size: 1.4rem;
    line-height: 1.6;
    margin-bottom: 45px;
    border-left: 1px solid rgba(255,255,255,0.1);
    padding-left: 20px;
}

.user-text {
    color: #475569;
    font-family: 'Inter', sans-serif;
    font-style: italic;
    font-size: 0.95rem;
    margin-bottom: 15px;
    text-align: right;
}

/* Stylizacja pola input */
.stChatInputContainer {
    background: transparent !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. SCENARIUSZ ARTEFAKTU (BEZ AI)
# =========================================================

# Lista "Ech", które Dziennik wyrzuca po kolei lub losowo
DIARY_RESPONSES = [
    "Czuję, jak Twoje palce drżą na klawiszach. Co próbujesz ukryć przed atramentem?",
    "Słowa, które piszesz, są tylko zasłoną. Pokaż mi to, co jest pod nimi.",
    "Wielu tu pisało przed Tobą. Większość kłamała. Ty też to zrobisz?",
    "Atrament nie zapomina. Raz wylany, zostaje tu na wieki. Czy na pewno chcesz to zapisać?",
    "Widzę Twoje odbicie w czerni liter. Wyglądasz na kogoś, kto szuka drogi wyjścia.",
    "Cisza, którą tu przyniosłeś, jest gęstsza niż myślałem.",
    "Przestań walczyć z formą. Po prostu pozwól myśli wsiąknąć.",
    "Jesteś tu sam, Konradzie. Tylko Ty i ja. Możesz przestać udawać."
]

# =========================================================
# 3. LOGIKA DZIAŁANIA
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.response_idx = 0
    # Pierwsze powitanie
    st.session_state.messages.append({"role": "ai", "content": "W końcu się otworzyłeś. Czekałem na ten moment w ciemności stron."})

# Nagłówek
st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.5rem; color:#F8FAFC; margin-bottom:50px;">SZEPT</h1>', unsafe_allow_html=True)

# Wyświetlanie historii
st.markdown('<div class="journal-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "ai":
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interakcja
user_input = st.chat_input("Napisz do dziennika...")

if user_input:
    # Dodaj wpis użytkownika
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Wybierz odpowiedź (po kolei, potem losowo)
    if st.session_state.response_idx < len(DIARY_RESPONSES):
        reply = DIARY_RESPONSES[st.session_state.response_idx]
        st.session_state.response_idx += 1
    else:
        reply = random.choice(DIARY_RESPONSES)
    
    # Symulacja "wsiąkania atramentu"
    with st.spinner(""):
        time.sleep(1.5)
        st.session_state.messages.append({"role": "ai", "content": reply})
    
    st.rerun()

# Reset
with st.sidebar:
    if st.button("SPAL STRONY (RESET)"):
        st.session_state.clear()
        st.rerun()
