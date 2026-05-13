import streamlit as st
import time
import random
import google.generativeai as genai

# =========================================================
# KONFIGURACJA AI & SZEPTU
# =========================================================

# TUTAJ WKLEJ SWÓJ KLUCZ
API_KEY = "AIzaSyCCtHo_I9MCk5ud7frk_wn3XnVhUM7EwAI" 

if API_KEY != "AIzaSyCCtHo_I9MCk5ud7frk_wn3XnVhUM7EwAI":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Brak klucza API. Wklej go w kodzie, aby AI mogło działać.")

st.set_page_config(page_title="SZEPT | AI", page_icon="🌙", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;1,400&family=Inter:wght@100;300;400&display=swap');
.stApp { background-color: #08080A; color: #94A3B8; font-family: 'Inter', sans-serif; }
.brand-header { text-align: center; padding: 60px 0 20px 0; }
.brand-name { font-size: 2.8rem; letter-spacing: 0.8rem; color: #F8FAFC; font-weight: 100; text-transform: uppercase; margin-bottom: 5px; }
.brand-tagline { font-family: 'Bodoni Moda', serif; font-style: italic; color: #475569; font-size: 0.9rem; letter-spacing: 0.1rem; }
.whisper-card { background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 2px; margin: 20px 0; text-align: center; }
.question-text { font-size: 1.3rem; color: #CBD5E1; line-height: 1.8; font-weight: 300; }
.aura-title { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.3rem; color: #64748B; margin-bottom: 10px; }
.aura-value { font-family: 'Bodoni Moda', serif; font-size: 1.8rem; color: #F1F5F9; margin-top: 5px; line-height: 1.4; }
textarea { background-color: transparent !important; border: none !important; border-bottom: 1px solid #1E293B !important; color: #F8FAFC !important; font-size: 1.1rem !important; text-align: center !important; }
.stButton > button { background: transparent !important; color: #64748B !important; border: 1px solid #1E293B !important; border-radius: 0px !important; padding: 0.5rem 2rem !important; transition: 0.5s; letter-spacing: 0.1rem; width: 100%; }
footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIKA AI ARCHITEKTA
# =========================================================

def analyze_aura_with_ai(answers):
    prompt = f"""
    Jesteś 'Architektem' w aplikacji SZEPT. Twoim zadaniem jest analiza profilu psychologicznego użytkownika na podstawie jego szczerych odpowiedzi.
    
    Odpowiedzi użytkownika:
    1. {answers[0]}
    2. {answers[1]}
    3. {answers[2]}

    Stwórz nazwę 'Aury' dla tego użytkownika (max 3 słowa). Aura musi być poetycka, minimalistyczna i trafiać w sedno emocji (np. 'Zasypana Tęsknota', 'Spokój Przed Burzą', 'Analityczna Cisza').
    Następnie dopisz jedno krótkie zdanie (max 10 słów), które wyjaśnia tę aurę.
    
    Format: Nazwa Aury | Opis
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Czysta Karta | Połączenie z Architektem zostało przerwane."

# =========================================================
# BANK PYTAŃ I SESJA
# =========================================================

QUESTION_BANK = [
    "Za czym tęskni Twoja głowa, kiedy w pokoju robi się zupełnie cicho?",
    "Opisz moment, w którym poczułeś, że nie musisz przed nikim niczego udawać.",
    "Czego najbardziej boisz się w kontakcie z nową osobą?",
    "Jaka prawda o Tobie jest najtrudniejsza do wypowiedzenia na głos?",
    "Co jest Twoim prywatnym schronieniem, gdy świat staje się zbyt głośny?"
]

if "questions" not in st.session_state:
    st.session_state.questions = random.sample(QUESTION_BANK, 3)
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.finished = False

# =========================================================
# INTERFEJS
# =========================================================

st.markdown("<div class='brand-header'><div class='brand-name'>SZEPT</div><div class='brand-tagline'>Where conversations breathe</div></div>", unsafe_allow_html=True)

if not st.session_state.finished:
    current_q = st.session_state.questions[st.session_state.step]
    st.markdown(f"<div class='whisper-card'><p class='question-text'>{current_q}</p></div>", unsafe_allow_html=True)
    ans = st.text_area("Twoja myśl", height=150, key=f"ans_{st.session_state.step}", label_visibility="collapsed")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Uwolnij szept"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step < len(st.session_state.questions) - 1:
                    st.session_state.step += 1
                else:
                    st.session_state.finished = True
                st.rerun()

else:
    with st.spinner("Architekt wsłuchuje się w Twoje echo..."):
        aura_raw = analyze_aura_with_ai(st.session_state.answers)
    
    if "|" in aura_raw:
        aura_name, aura_desc = aura_raw.split("|")
    else:
        aura_name, aura_desc = aura_raw, ""

    st.markdown(f"""
        <div class='whisper-card'>
            <p class='aura-title'>Twoja Aura</p>
            <p class='aura-value'>{aura_name.strip()}</p>
            <p style='color: #475569; font-size: 0.9rem; margin-top: 10px;'>{aura_desc.strip()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #1E293B;'><p style='text-align:center; color:#1E293B; letter-spacing:0.2rem; font-size:0.7rem;'>SESJA ODPOCZYWA</p>", unsafe_allow_html=True)

    rc1, rc2, rc3 = st.columns([1, 1, 1])
    with rc2:
        if st.button("Powróć do rytuału"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
            
