import streamlit as st
import google.generativeai as genai
import time

# =========================================================
# 1. BAZA DANYCH AURY (TEST STATYCZNY)
# =========================================================

QUESTIONS_DATABASE = [
    {
        "pytanie": "Gdy wchodzisz do pustego, starego domu, co czujesz najpierw?",
        "opcje": {
            "A": "Zapach kurzu i wilgoci.",
            "B": "Ciężar historii i echo dawnych rozmów.",
            "C": "Możliwości aranżacji i stan techniczny ścian."
        }
    },
    {
        "pytanie": "Wybierz przedmiot, który najlepiej Cię definiuje:",
        "opcje": {
            "A": "Szklany pryzmat rozszczepiający światło.",
            "B": "Surowy, dębowy stół.",
            "C": "Srebrny kompas, który zawsze wskazuje północ."
        }
    },
    {
        "pytanie": "Jak reagujesz na nagłą, głośną burzę?",
        "opcje": {
            "A": "Zamykam okna, sprawdzam bezpieczniki.",
            "B": "Staję przy oknie, by poczuć drżenie powietrza.",
            "C": "Ignoruję ją, skupiam się na tym, co robię."
        }
    }
]

# =========================================================
# 2. SILNIK AI (DLA FINAŁU)
# =========================================================

API_KEY = "TWOJ_KLUCZ_AIZA_TUTAJ"
genai.configure(api_key=API_KEY)

def szept_final_question(user_profile):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        persona = (
            "Jesteś Dziennikiem Badawczym. Otrzymałeś wyniki testu aury użytkownika. "
            "Twoim zadaniem jest podsumować te wyniki jednym zdaniem i zadać OSTATECZNE, "
            "głębokie pytanie, które zmusi go do autorefleksji. Bądź chłodny i celny. Max 20 słów."
        )
        prompt = f"PROFIL UŻYTKOWNIKA: {user_profile}\n\nZadaj finałowe pytanie."
        response = model.generate_content(f"SYSTEM: {persona}\n{prompt}")
        return response.text
    except:
        return "Twoja aura jest zbyt gęsta na słowa. Czego się boisz?"

# =========================================================
# 3. DESIGN I LOGIKA STREAMLIT
# =========================================================

st.set_page_config(page_title="SZEPT", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@100&display=swap');
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #050505 !important; color: #eee; }
    .stButton>button { background-color: transparent; border: 1px solid #333; color: #888; width: 100%; transition: 0.5s; }
    .stButton>button:hover { border-color: #eee; color: #eee; }
    .question-title { font-family: 'Bodoni Moda', serif; font-size: 1.8rem; text-align: center; margin-bottom: 2rem; font-style: italic; }
</style>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.final_msg = None

# --- FAZA I: TEST STATYCZNY ---
if st.session_state.step < len(QUESTIONS_DATABASE):
    current_q = QUESTIONS_DATABASE[st.session_state.step]
    st.markdown(f'<div class="question-title">{current_q["pytanie"]}</div>', unsafe_allow_html=True)
    
    for key, val in current_q["opcje"].items():
        if st.button(val):
            st.session_state.answers.append(val)
            st.session_state.step += 1
            st.rerun()

# --- FAZA II: PRZEBUDZENIE AI ---
elif st.session_state.step == len(QUESTIONS_DATABASE):
    if not st.session_state.final_msg:
        with st.spinner(" "):
            profile = " | ".join(st.session_state.answers)
            st.session_state.final_msg = szept_final_question(profile)
            st.session_state.step += 1
            st.rerun()

# --- FAZA III: EKRAN FINAŁOWY ---
else:
    st.markdown(f'<div class="question-title">{st.session_state.final_msg}</div>', unsafe_allow_html=True)
    if st.button("SPAL DZIENNIK I ZACZNIJ OD NOWA"):
        st.session_state.clear()
        st.rerun()
