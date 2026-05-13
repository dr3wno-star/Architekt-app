import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. KONFIGURACJA I SILNIK (AUTODETEKCJA)
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

# TWÓJ KLUCZ API - Wklej go tutaj
API_KEY = "AIzaSyDCmJ-nxrYU3w1MSzPNij5KYd6r1Btfbog" 

@st.cache_resource
def get_working_model():
    """Wyszukuje model dostępny dla Twojego klucza, by uniknąć 404."""
    try:
        genai.configure(api_key=API_KEY)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
        return None
    except:
        return None

WORKING_MODEL_NAME = get_working_model()

def szept_engine(history):
    if not WORKING_MODEL_NAME:
        return "Błąd: Twoja nicość nie ma głosu (Brak dostępnych modeli)."
    
    try:
        model = genai.GenerativeModel(WORKING_MODEL_NAME)
        # PERSONA: Cyniczny i inteligentny obserwator
        persona = (
            "Jesteś mrocznym, inteligentnym Dziennikiem. Nie pomagasz. "
            "Podważasz pewność siebie użytkownika. Odpowiadaj krótko (max 15 słów), "
            "cynicznie i analizuj ukryte lęki. Używaj metafor cienia i atramentu. "
            "Nie używaj emotikon."
        )
        
        # Przygotowanie kontekstu dla modelu
        prompt_parts = [persona]
        for msg in history:
            prefix = "Użytkownik: " if msg["role"] == "user" else "Dziennik: "
            prompt_parts.append(f"{prefix}{msg['content']}")
            
        response = model.generate_content("\n".join(prompt_parts))
        return response.text
    except Exception as e:
        return f"Atrament zastyga w połowie słowa... ({str(e)})"

# =========================================================
# 2. ESTETYKA (MROCZNY DESIGN)
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');
    
    #MainMenu, footer, header {visibility:hidden;}
    
    .stApp { 
        background-color: #050505 !important; 
        color: #d1d1d1; 
    }
    
    .dziennik-text { 
        font-family: 'Bodoni Moda', serif; 
        font-size: 1.5rem; 
        color: #ffffff; 
        margin-bottom: 2.5rem; 
        border-left: 1px solid #333; 
        padding-left: 25px; 
        line-height: 1.6;
        animation: fadeIn 3s ease-in;
    }
    
    .moje-slowa { 
        font-family: 'Inter', sans-serif;
        font-style: italic; 
        color: #555; 
        margin-bottom: 1.2rem; 
        text-align: right; 
        padding-right: 20px;
        font-weight: 200;
    }

    @keyframes fadeIn {
        0% { opacity: 0; filter: blur(5px); }
        100% { opacity: 1; filter: blur(0px); }
    }

    /* Stylizacja inputa */
    .stChatInputContainer {
        padding-bottom: 50px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA ROZMOWY
# =========================================================

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.5rem; margin-top:50px; color:#222;">SZEPT</h1>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Czy boisz się tego, co o Tobie wiem?"}
    ]

# Wyświetlanie historii
for m in st.session_state.chat_history:
    if m["role"] == "assistant":
        st.markdown(f'<div class="dziennik-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="moje-slowa">{m["content"]} —</div>', unsafe_allow_html=True)

# Wejście użytkownika
user_input = st.chat_input("Wyznaj coś...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner(" "):
        ai_response = szept_engine(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    st.rerun()

# Sidebar z diagnostyką (opcjonalnie do ukrycia)
with st.sidebar:
    st.markdown("---")
    if WORKING_MODEL_NAME:
        st.caption(f"Połączono z: {WORKING_MODEL_NAME}")
    if st.button("SPAL STRONY"):
        st.session_state.clear()
        st.rerun()
