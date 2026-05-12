import streamlit as st
import time

# =========================================================
# KONFIGURACJA SZEPTU
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="🌙", layout="centered")

# CSS: Estetyka wyciszenia i oddechu
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;1,400&family=Inter:wght@100;300;400&display=swap');

.stApp {
    background-color: #08080A;
    color: #94A3B8;
    font-family: 'Inter', sans-serif;
}

.brand-header {
    text-align: center;
    padding: 60px 0 20px 0;
}

.brand-name {
    font-size: 2.8rem;
    letter-spacing: 0.8rem;
    color: #F8FAFC;
    font-weight: 100;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.brand-tagline {
    font-family: 'Bodoni Moda', serif;
    font-style: italic;
    color: #475569;
    font-size: 0.9rem;
    letter-spacing: 0.1rem;
}

.whisper-card {
    background: rgba(255, 255, 255, 0.01);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 40px;
    border-radius: 2px;
    margin: 20px 0;
    text-align: center;
}

.question-text {
    font-size: 1.3rem;
    color: #CBD5E1;
    line-height: 1.8;
    font-weight: 300;
}

.aura-title {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.3rem;
    color: #64748B;
    margin-bottom: 10px;
}

.aura-value {
    font-family: 'Bodoni Moda', serif;
    font-size: 2.2rem;
    color: #F1F5F9;
    margin-top: 5px;
}

/* Stylizacja pól tekstowych */
textarea {
    background-color: transparent !important;
    border: none !important;
    border-bottom: 1px solid #1E293B !important;
    color: #F8FAFC !important;
    font-size: 1.1rem !important;
    text-align: center !important;
}

/* Przyciski */
.stButton > button {
    background: transparent !important;
    color: #64748B !important;
    border: 1px solid #1E293B !important;
    border-radius: 0px !important;
    padding: 0.5rem 2rem !important;
    transition: 0.5s;
    letter-spacing: 0.1rem;
    width: 100%;
}

.stButton > button:hover {
    color: #F8FAFC !important;
    border-color: #334155 !important;
    background: rgba(255,255,255,0.02) !important;
}

footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIKA ARCHITEKTA
# =========================================================

QUESTIONS = [
    "Za czym tęskni Twoja głowa, kiedy w pokoju robi się zupełnie cicho?",
    "Opisz moment, w którym poczułeś, że nie musisz przed nikim niczego udawać.",
    "Czego najbardziej boisz się w kontakcie z nową osobą?",
    "Gdyby Twój obecny stan ducha był kolorem lub dźwiękiem – co by to było?"
]

def analyze_aura(answers):
    text = " ".join(answers).lower()
    auras = []
    
    if any(w in text for w in ["spokój", "cisza", "bezpiecz", "powol", "oddech"]):
        auras.append("Spokojna Obecność")
    if any(w in text for w in ["myśl", "analiz", "dlaczego", "wnętrze", "tęskni"]):
        auras.append("Refleksyjna Energia")
    if any(w in text for w in ["boję", "trudno", "ukrywam", "ostrożn", "zran"]):
        auras.append("Emocjonalna Ostrożność")
    if any(w in text for w in ["prawda", "dusza", "rezonans", "głęb", "sens"]):
        auras.append("Głębokie Połączenie")
        
    return auras[:2] if auras else ["Czysta Karta"]

# =========================================================
# SYSTEM SESJI
# =========================================================

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.finished = False

# =========================================================
# INTERFEJS
# =========================================================

st.markdown("""
    <div class='brand-header'>
        <div class='brand-name'>SZEPT</div>
        <div class='brand-tagline'>Where conversations breathe</div>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.finished:
    st.write("")
    current_q = QUESTIONS[st.session_state.step]
    
    st.markdown(f"<div class='whisper-card'><p class='question-text'>{current_q}</p></div>", unsafe_allow_html=True)
    
    # Pole tekstowe bez labela
    ans = st.text_area("Twoja myśl", height=150, key=f"ans_{st.session_state.step}", label_visibility="collapsed")
    
    st.write("")
    # Wyśrodkowany przycisk
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Uwolnij szept"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step < len(QUESTIONS) - 1:
                    st.session_state.step += 1
                else:
                    st.session_state.finished = True
                st.rerun()
            else:
                st.warning("Pozwól myślom zamienić się w słowa.")

else:
    # EKRAN ANALIZY
    with st.spinner("Architekt kalibruje Twój rezonans..."):
        time.sleep(2)
    
    user_auras = analyze_aura(st.session_state.answers)
    
    st.markdown(f"""
        <div class='whisper-card'>
            <p class='aura-title'>Twoja Aura</p>
            <p class='aura-value'>{' • '.join(user_auras)}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='text-align:center; font-style:italic; color:#475569; font-size:0.8rem;'>Twoje echo zostało wysłane w przestrzeń. Nie szukaj nikogo. Pozwól rezonansowi działać.</p>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<hr style='border-color: #1E293B;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#1E293B; letter-spacing:0.2rem; font-size:0.7rem;'>SESJA ODPOCZYWA</p>", unsafe_allow_html=True)

    st.write("")
    c1, c2, c3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Powróć do rytuału"):
            st.session_state.step = 0
            st.session_state.answers = []
            st.session_state.finished = False
            st.rerun()
            
