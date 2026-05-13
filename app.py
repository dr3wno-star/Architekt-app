import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. RDZEŃ DIAGNOSTYCZNY (BACK-TO-BASICS)
# =========================================================

st.set_page_config(page_title="SZEPT", layout="centered")

# TWÓJ KLUCZ API
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
        
        # PROTOKÓŁ: Sekwencyjna Inwigilacja Aury
        persona = (
            "Jesteś Dziennikiem Badawczym. Twoim celem jest przeprowadzenie wywiadu profilującego aurę. "
            "ZASADA: Na podstawie ostatniej odpowiedzi użytkownika zadaj jedno, celne pytanie, "
            "które pogłębi analizę jego temperamentu i energii. "
            "Zaczynaj od pytań luźnych, przechodząc w coraz bardziej kierunkowe i intymne. "
            "Nie wyciągaj jeszcze wniosków. Tylko pytaj. Krótko, chłodno, precyzyjnie. Max 15 słów."
        )
        
        context = f"SYSTEM: {persona}\n\n"
        for msg in history:
            role = "Użytkownik" if msg["role"] == "user" else "Dziennik"
            context += f"{role}: {msg['content']}\n"
            
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Przerwanie skanu: {str(e)}"

# =========================================================
# 2. DESIGN (SUROWY MINIMALIZM)
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400&display=swap');
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #050505 !important; color: #888; }
    
    .question-box { 
        font-family: 'Inter', sans-serif; 
        font-size: 1.4rem; 
        color: #eee; 
        margin-top: 100px;
        margin-bottom: 50px; 
        text-align: center;
        font-weight: 200;
        letter-spacing: 1px;
    }
    
    .history-text { 
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #333; 
        margin-bottom: 5px; 
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. INTERFEJS
# =========================================================

if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "assistant", "content": "Gdybyś był zapachem w opuszczonym domu, czym byś był?"}
    ]

# Wyświetlamy tylko ostatnie pytanie na środku (focus mode)
last_question = st.session_state.chat[-1]["content"]
st.markdown(f'<div class="question-box">{last_question}</div>', unsafe_allow_html=True)

# Historia (mały druk na dole dla kontekstu)
with st.expander("Ślad Twoich odpowiedzi"):
    for m in st.session_state.chat[:-1]:
        prefix = "— " if m["role"] == "user" else ""
        st.markdown(f'<div class="history-text">{prefix}{m["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Odpowiedz...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.spinner(" "):
        next_q = get_next_question(st.session_state.chat)
        st.session_state.chat.append({"role": "assistant", "content": next_q})
    st.rerun()

if st.sidebar.button("ZACZNIJ OD NOWA"):
    st.session_state.clear()
    st.rerun()
