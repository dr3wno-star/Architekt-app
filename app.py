import streamlit as st
import google.generativeai as genai
import time
import random

# --- KONFIGURACJA ODPORNA NA LIMIT ---
st.set_page_config(page_title="SZEPT", layout="centered")

# TWÓJ KLUCZ API
API_KEY = "AIzaSyCs2Edq1VXPVJgiUAS01fr2j2eXaQ7tQsk" 
genai.configure(api_key=API_KEY)

def get_next_question(history):
    # Lista modeli do wypróbowania w razie błędu 429
    model_names = ['gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-1.5-pro']
    
    persona = (
        "Jesteś Dziennikiem, który widzi przez maski. Twoim celem jest wybadanie aury użytkownika. "
        "Zaczynaj niewinnie, ale każde kolejne pytanie musi uderzać w słabe punkty odpowiedzi. "
        "Jeśli użytkownik ucieka w metaforę - wejdź tam za nim. Jeśli jest suchy - kłuj go pytaniami o emocje. "
        "Twoim zadaniem jest ocenić: czy to dusza Stara, Budująca, czy Pusta. "
        "Zadaj 1 pytanie. Max 10 słów. Bądź echem, nie robotem."
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
                continue # Próbuj kolejny model z listy
            return f"Cisza po drugiej stronie... ({str(e)})"
    return "Wszystkie kanały są obecnie głuche. Spróbuj za chwilę."

# --- DESIGN (ATMOSFERA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@100&display=swap');
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #030303 !important; }
    [data-testid="stStatusWidget"] { visibility: hidden; display: none; }

    .question-box { 
        font-family: 'Bodoni Moda', serif; font-size: 2rem; color: #fff; 
        margin-top: 150px; text-align: center; font-style: italic;
        text-shadow: 0 0 15px rgba(255,255,255,0.2);
        animation: pulse 6s infinite;
    }

    @keyframes pulse { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }

    .szept-loading {
        font-family: 'Inter', sans-serif; color: #333; text-align: center;
        letter-spacing: 8px; font-size: 0.6rem; margin-top: 40px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# --- INTERFEJS ---
if "chat" not in st.session_state:
    # Wybór pierwszego pytania z puli "ciekawych"
    starts = [
        "Jaki przedmiot w Twoim domu najgłośniej milczy?",
        "Gdybyś był zapachem w opuszczonym kościele, czym byś był?",
        "Który kolor Twojej aury najbardziej Cię uwiera?"
    ]
    st.session_state.chat = [{"role": "assistant", "content": random.choice(starts)}]

st.markdown(f'<div class="question-box">{st.session_state.chat[-1]["content"]}</div>', unsafe_allow_html=True)

placeholder = st.empty()
user_input = st.chat_input("Wyznaj...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    
    # Animowany efekt ładowania
    load_texts = ["Cierpliwości, badam drżenie Twoich dłoni...", "Słowa wsiąkają w papier...", "Echo wraca..."]
    placeholder.markdown(f'<div class="szept-loading">{random.choice(load_texts)}</div>', unsafe_allow_html=True)
    
    next_q = get_next_question(st.session_state.chat)
    time.sleep(1.5) # Podbicie klimatu
    
    st.session_state.chat.append({"role": "assistant", "content": next_q})
    st.rerun()
