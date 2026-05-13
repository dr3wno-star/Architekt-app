import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. KONFIGURACJA SILNIKA ANALIZY AURY
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

# TWÓJ KLUCZ API (Wklej go między cudzysłów)
API_KEY = "AIzaSyDCmJ-nxrYU3w1MSzPNij5KYd6r1Btfbog" 

@st.cache_resource
def initialize_engine():
    """Inicjalizuje połączenie i znajduje dostępny model."""
    try:
        genai.configure(api_key=API_KEY)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
        return None
    except:
        return None

WORKING_MODEL = initialize_engine()

def analyze_aura(history):
    if not WORKING_MODEL:
        return "System nie widzi Twojej aury. Sprawdź klucz API."
    
    try:
        model = genai.GenerativeModel(WORKING_MODEL)
        
        # DEFINICJA OSOBOWOŚCI: Zimny Analityk Aury
        persona = (
            "Jesteś Dziennikiem, który przeprowadza zimną analizę psychologiczną (Cold Reading). "
            "Nie bełkoczesz o mroku i nicości. Badasz 'aurę' użytkownika na podstawie jego słów. "
            "Twoim zadaniem jest ocenić jego obecny stan: agresję, lęk, arogancję lub zagubienie. "
            "Mów o pęknięciach w jego postawie, ciężarze emocjonalnym i barwie intencji. "
            "Bądź bezlitosny, rzeczowy i konkretny. Maksymalnie 15 słów. Żadnych ozdobników."
        )
        
        # Budowanie kontekstu dla Gemini
        context = f"SYSTEM: {persona}\n\n"
        for msg in history:
            role = "Użytkownik" if msg["role"] == "user" else "Dziennik"
            context += f"{role}: {msg['content']}\n"
            
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Aura zbyt gęsta, by ją przejrzeć... ({str(e)})"

# =========================================================
# 2. DESIGN (ESTETYKA MINIMALIZMU)
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');
    
    #MainMenu, footer, header {visibility:hidden;}
    
    .stApp { 
        background-color: #050505 !important; 
        color: #e0e0e0; 
    }
    
    .journal-entry { 
        font-family: 'Bodoni Moda', serif; 
        font-size: 1.5rem; 
        color: #ffffff; 
        margin-bottom: 3rem; 
        border-left: 1px solid #444; 
        padding-left: 25px; 
        line-height: 1.6;
        animation: emerge 2.5s ease-out;
    }
    
    .user-echo { 
        font-family: 'Inter', sans-serif;
        font-style: italic; 
        color: #555; 
        margin-bottom: 1.5rem; 
        text-align: right; 
        padding-right: 20px;
        font-weight: 200;
    }

    @keyframes emerge {
        0% { opacity: 0; filter: blur(8px); transform: translateY(5px); }
        100% { opacity: 1; filter: blur(0px); transform: translateY(0px); }
    }

    /* Ukrycie obramowania inputa dla czystego efektu */
    .stChatInputContainer {
        border-top: 1px solid #111 !important;
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. INTERFEJS I LOGIKA
# =========================================================

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.5rem; margin-top:60px; color:#1a1a1a;">SZEPT</h1>', unsafe_allow_html=True)

if "journal_state" not in st.session_state:
    st.session_state.journal_state = [
        {"role": "assistant", "content": "Czy boisz się tego, co Twoja aura mówi o Tobie dzisiaj?"}
    ]

# Renderowanie rozmowy
for m in st.session_state.journal_state:
    if m["role"] == "assistant":
        st.markdown(f'<div class="journal-entry">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-echo">{m["content"]} —</div>', unsafe_allow_html=True)

# Obsługa wejścia
user_input = st.chat_input("Napisz coś, bym mógł Cię przejrzeć...")

if user_input:
    st.session_state.journal_state.append({"role": "user", "content": user_input})
    with st.spinner(" "):
        analysis = analyze_aura(st.session_state.journal_state)
        st.session_state.journal_state.append({"role": "assistant", "content": analysis})
    st.rerun()

# Funkcje pomocnicze w sidebarze
with st.sidebar:
    st.markdown("### Status Analizy")
    if WORKING_MODEL:
        st.success(f"Oczy otwarte ({WORKING_MODEL})")
    else:
        st.error("Dziennik jest ślepy (Brak modelu)")
    
    if st.button("RESETUJ AURĘ"):
        st.session_state.clear()
        st.rerun()
