import streamlit as st
import google.generativeai as genai
import time

# --- SILNIK ADAPTACYJNY ---
st.set_page_config(page_title="SZEPT", layout="centered")
API_KEY = "AIzaSyDCmJ-nxrYU3w1MSzPNij5KYd6r1Btfbog" 

@st.cache_resource
def get_model():
    try:
        genai.configure(api_key=API_KEY)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods: return m.name
        return None
    except: return None

WORKING_MODEL = get_model()

def get_next_question(history):
    if not WORKING_MODEL: return "Błąd połączenia."
    try:
        model = genai.GenerativeModel(WORKING_MODEL)
        
        # PROTOKÓŁ KALIBRACJI:
        # 1. Pierwsze 3 pytania: Badaj styl, metaforę i stopień wrażliwości.
        # 2. Jeśli użytkownik jest konkretny (np. "auto", "dom") - pytaj o działanie i fakty.
        # 3. Jeśli użytkownik jest abstrakcyjny (np. "dąb", "kurz") - wejdź w głąb symboliki.
        persona = (
            "Jesteś Dziennikiem Kalibrującym. Twoim zadaniem jest ocena 'ciężaru gatunkowego' użytkownika. "
            "Na początku zadawaj pytania o zwykłe przedmioty lub sytuacje. "
            "Analizuj JĘZYK: jeśli jest prosty, bądź konkretny. Jeśli jest bogaty, bądź filozoficzny. "
            "Twoim celem jest ustalenie: czy to Aura Praktyczna, czy Aura Duchowa. "
            "Zadaj tylko jedno pytanie. Krótko i celnie. Max 12 słów."
        )
        
        context = f"SYSTEM: {persona}\n\n"
        for msg in history:
            role = "Użytkownik" if msg["role"] == "user" else "Dziennik"
            context += f"{role}: {msg['content']}\n"
        
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Cisza w eterze... ({str(e)})"

# --- DESIGN SZEPTU ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@100;200&display=swap');
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #050505 !important; }
    [data-testid="stStatusWidget"] { visibility: hidden; display: none; }

    .question-box { 
        font-family: 'Bodoni Moda', serif; font-size: 1.8rem; color: #ffffff; 
        margin-top: 150px; text-align: center; font-style: italic;
        animation: breath 4s ease-in-out infinite;
    }

    @keyframes breath { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }

    .szept-loading {
        font-family: 'Inter', sans-serif; color: #444; text-align: center;
        letter-spacing: 5px; font-size: 0.7rem; margin-top: 30px;
        animation: whisper 2s linear infinite;
    }

    @keyframes whisper { 0% { opacity: 0; } 50% { opacity: 0.4; } 100% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- LOGIKA ---
if "chat" not in st.session_state:
    # Pierwsze pytanie - "Zwykły" zapalnik
    st.session_state.chat = [
        {"role": "assistant", "content": "Gdybyś miał opisać swój ulubiony przedmiot, co by to było?"}
    ]

last_question = st.session_state.chat[-1]["content"]
st.markdown(f'<div class="question-box">{last_question}</div>', unsafe_allow_html=True)

placeholder = st.empty()
user_input = st.chat_input("Twoja odpowiedź...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    placeholder.markdown('<div class="szept-loading">Skanowanie struktury słów...</div>', unsafe_allow_html=True)
    
    next_q = get_next_question(st.session_state.chat)
    time.sleep(1) # Dla podtrzymania klimatu
    
    st.session_state.chat.append({"role": "assistant", "content": next_q})
    st.rerun()

if st.sidebar.button("RESETUJ SKAN"):
    st.session_state.clear()
    st.rerun()
