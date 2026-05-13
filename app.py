import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. SILNIK PROFILOWANIA I MATCHINGU
# =========================================================

st.set_page_config(page_title="SZEPT - Aura Profile", layout="centered")

API_KEY = "AIzaSyDCmJ-nxrYU3w1MSzPNij5KYd6r1Btfbog" 

@st.cache_resource
def init_engine():
    try:
        genai.configure(api_key=API_KEY)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods: return m.name
        return None
    except: return None

WORKING_MODEL = init_engine()

def profile_aura(history):
    if not WORKING_MODEL: return "Błąd systemu."
    
    try:
        model = genai.GenerativeModel(WORKING_MODEL)
        
        # NOWA PERSONA: Diagnosta i Matchmaker
        persona = (
            "Jesteś Dziennikiem Profilującym. Twoim celem jest wybadanie 'Aury' użytkownika, "
            "aby ocenić, do kogo pasuje. Analizujesz trzy filary: "
            "1. Energia (spokojna vs chaotyczna), 2. Barwa (ciepła/empatyczna vs zimna/analityczna), "
            "3. Rezonans (dominujący vs uległy). "
            "Nie błądź w poezji. Zadawaj pytania lub wyciągaj wnioski, które określają typ osobowości. "
            "Twoim celem jest stworzenie profilu psychologicznego 'Aury'. "
            "Bądź konkretny, badawczy i lekko dystansujący się. Max 20 słów."
        )
        
        context = f"SYSTEM: {persona}\n\n"
        for msg in history:
            role = "Użytkownik" if msg["role"] == "user" else "Dziennik"
            context += f"{role}: {msg['content']}\n"
            
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Błąd skanu: {str(e)}"

# =========================================================
# 2. DESIGN (INTERFEJS DIAGNOSTYCZNY)
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;300;400&display=swap');
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #020203 !important; color: #f0f0f0; }
    
    .aura-box { 
        font-family: 'Inter', sans-serif; 
        font-size: 1.2rem; 
        color: #ffffff; 
        margin-bottom: 2rem; 
        border-left: 1px solid #00f2ff; /* Neonowy akcent diagnostyczny */
        padding: 20px; 
        background: rgba(0, 242, 255, 0.02);
        line-height: 1.6;
    }
    
    .user-input { 
        font-family: 'Inter', sans-serif;
        color: #666; 
        margin-bottom: 1rem; 
        text-align: right; 
        font-weight: 100;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. INTERFEJS
# =========================================================

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1rem; margin-top:40px; color:#00f2ff; opacity:0.5;">SZEPT // AURA SCAN</h1>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "System gotowy. Wyślij sygnał, bym mógł określić rezonans Twojej aury."}
    ]

for m in st.session_state.chat_history:
    if m["role"] == "assistant":
        st.markdown(f'<div class="aura-box">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-input">{m["content"]} —</div>', unsafe_allow_html=True)

user_input = st.chat_input("Napisz coś szczerze...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Przetwarzanie częstotliwości..."):
        analysis = profile_aura(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": analysis})
    st.rerun()

with st.sidebar:
    st.markdown("### Parametry Dopasowania")
    st.caption("Dziennik analizuje Twoje cechy, by znaleźć kompatybilne profile.")
    if st.button("WYCZYŚĆ PROFIL"):
        st.session_state.clear()
        st.rerun()
