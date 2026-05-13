import streamlit as st
import google.generativeai as genai
import time
import random

# =========================================================
# 1. KONFIGURACJA I ODPORNOŚĆ NA BŁĘDY
# =========================================================

st.set_page_config(page_title="SZEPT", layout="centered")

# TWOJE SERCE SYSTEMU (KLUCZ API)
API_KEY = "AIzaSyCs2Edq1VXPVJgiUAS01fr2j2eXaQ7tQsk" 
genai.configure(api_key=API_KEY)

def get_next_question(history):
    # Lista modeli - jeśli jeden ma limit (429), system bierze kolejny
    model_names = ['gemini-1.5-flash', 'gemini-1.0-pro']
    
    persona = (
        "Jesteś Dziennikiem Badawczym. Twoim celem jest wybadanie aury użytkownika. "
        "ZACZNIJ OD ZWYKŁYCH RZECZY. Pierwsze pytania muszą być o przedmioty, dom, codzienne wybory. "
        "Analizuj język: jeśli użytkownik odpowiada prosto, trzymaj się konkretów. "
        "Jeśli użytkownik odpowiada głęboko, metaforami - powoli wchodź w głąb jego psychiki. "
        "Zadaj tylko 1 pytanie. Max 12 słów. Nie bądź nachalny, bądź intrygujący."
    )
    
    context = f"SYSTEM: {persona}\n\n"
    for msg in history:
        role = "Użytkownik" if msg["role"] == "user" else "Dziennik"
        context += f"{role}: {msg['content']}\n"

    for m_name in model_names:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(context)
            return response.text
        except Exception as e:
            if "429" in str(e):
                continue
            return f"Echo nie wraca... ({str(e)})"
    return "Cisza. Spróbuj za moment, gdy atrament wyschnie."

# =========================================================
# 2. DESIGN - KLIMATYCZNY INTERFEJS
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@100&display=swap');
    
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #050505 !important; }
    
    /* Ukrycie standardowego spinnera Streamlit */
    [data-testid="stStatusWidget"] { visibility: hidden; display: none; }

    .question-box { 
        font-family: 'Bodoni Moda', serif; font-size: 1.8rem; color: #ffffff; 
        margin-top: 150px; text-align: center; font-style: italic;
        letter-spacing: 1px;
        animation: focusPulse 5s infinite;
    }

    @keyframes focusPulse {
        0%, 100% { opacity: 0.6; filter: blur(1px); }
        50% { opacity: 1; filter: blur(0px); }
    }

    .szept-loading {
        font-family: 'Inter', sans-serif; color: #333; text-align: center;
        letter-spacing: 6px; font-size: 0.7rem; margin-top: 40px;
        text-transform: uppercase;
        animation: whisperFade 2s infinite;
    }

    @keyframes whisperFade { 0%, 100% { opacity: 0.2; } 50% { opacity: 0.6; } }

    .stChatInputContainer { border-top: 1px solid #111 !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA DZIAŁANIA
# =========================================================

if "chat" not in st.session_state:
    # "Uziemione" starty, które zrozumie każdy
    starts = [
        "Jaki przedmiot, który masz pod ręką, najbardziej do Ciebie pasuje?",
        "Gdybyś miał opisać swój ulubiony zakątek w domu, co by to było?",
        "Jaki dźwięk kojarzy Ci się z absolutnym spokojem?",
        "Gdybyś miał dziś zatrzymać jeden moment, co by to było?"
    ]
    st.session_state.chat = [{"role": "assistant", "content": random.choice(starts)}]

# Wyświetlanie aktualnego pytania
st.markdown(f'<div class="question-box">{st.session_state.chat[-1]["content"]}</div>', unsafe_allow_html=True)

placeholder = st.empty()
user_input = st.chat_input("Napisz...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    
    # Klimatyczne ładowanie
    placeholder.markdown('<div class="szept-loading">Słucham...</div>', unsafe_allow_html=True)
    
    next_q = get_next_question(st.session_state.chat)
    time.sleep(1) # Chwila na oddech
    
    st.session_state.chat.append({"role": "assistant", "content": next_q})
    st.rerun()

# Dyskretny reset w sidebarze
if st.sidebar.button("ZACZNIJ OD NOWA"):
    st.session_state.clear()
    st.rerun()
