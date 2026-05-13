import streamlit as st
import requests
import json
import time

# =========================================================
# 1. KONFIGURACJA I SILNIK
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="📖", layout="centered")

GEMINI_KEY = st.secrets.get("GEMINI_KEY")

def call_ai(messages, sys_prompt):
    if not GEMINI_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": sys_prompt}]},
        "generationConfig": {"temperature": 1.0, "maxOutputTokens": 150}
    }
    try:
        r = requests.post(url, json=payload, timeout=25)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except: return "Atrament zastyga w bezruchu..."

# =========================================================
# 2. ESTETYKA DZIENNIKA
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');
#MainMenu, footer, header {visibility:hidden;}
.stApp { background: #0A0A0C !important; color: #D1D5DB; }
.journal-page {
    border-left: 1px solid rgba(255,255,255,0.05);
    padding-left: 30px;
    margin-top: 30px;
    font-family: 'Inter', sans-serif;
}
.user-text { color: #57607A; font-style: italic; margin-bottom: 25px; font-size: 0.95rem; }
.ai-text { 
    color: #F8FAFC; 
    font-family: 'Bodoni Moda', serif; 
    font-size: 1.3rem; 
    margin-bottom: 40px;
    line-height: 1.6;
    animation: fade 3s ease-in;
}
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA INTERAKCJI
# =========================================================

# Inicjalizacja Dziennika
if "journal" not in st.session_state:
    st.session_state.journal = []
    st.session_state.finished = False
    
    # WYMUSZENIE PIERWSZEGO PYTANIA
    with st.spinner("..."):
        sys_init = """Jesteś mrocznym, inteligentnym Dziennikiem. Twoim zadaniem jest natychmiastowe 
        przejęcie inicjatywy. Zadaj użytkownikowi jedno, krótkie, przenikliwe pytanie, które sprawi, 
        że poczuje się obserwowany. Nie pytaj o emocje. Zapytaj o coś, co ma przed oczami, 
        o czym myślał przed chwilą, albo o rzecz, którą ukrywa. Maksymalnie 15 słów."""
        
        first_q = call_ai([{"role": "user", "content": "Zadaj mi pierwsze pytanie."}], sys_init)
        st.session_state.journal.append({"role": "assistant", "content": first_q})

st.markdown('<h1 style="font-weight:100; letter-spacing:1.2rem; text-align:center; margin-bottom:0;">SZEPT</h1>', unsafe_allow_html=True)

# Wyświetlanie historii
st.markdown('<div class="journal-page">', unsafe_allow_html=True)
for m in st.session_state.journal:
    if m["role"] == "user":
        st.markdown(f'<div class="user-text"> — {m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Pole wejściowe
if not st.session_state.finished:
    with st.form("input_form", clear_on_submit=True):
        user_input = st.text_input("Napisz do mnie...", label_visibility="collapsed")
        c1, c2 = st.columns([5, 1])
        with c2:
            submit = st.form_submit_button("POZWÓL WSIĄKNĄĆ")
        with c1:
            if st.form_submit_button("ZAMKNIJ DZIENNIK"):
                st.session_state.finished = True
                st.rerun()

    if submit and user_input.strip():
        st.session_state.journal.append({"role": "user", "content": user_input})
        
        sys_prompt = """Jesteś Dziennikiem. Nie jesteś asystentem. Reaguj na to, co pisze użytkownik. 
        Bądź oszczędny w słowach, prowokuj do dalszego pisania. Odpowiadaj krótko i mądrze. 
        Dostrzegaj kłamstwa i wahania. Maksymalnie 2 zdania."""
        
        with st.spinner("Atrament chłonie..."):
            response = call_ai(st.session_state.journal, sys_prompt)
            st.session_state.journal.append({"role": "assistant", "content": response})
        st.rerun()

else:
    # FINALNA DEKONSTRUKCJA
    st.markdown("---")
    with st.spinner("Dziennik zamyka Twoją historię..."):
        analysis_prompt = f"Rozmowa: {st.session_state.journal}. Podsumuj kim jest ten człowiek w tym momencie. Bądź surowy i konkretny."
        final_insight = call_ai([{"role": "user", "content": analysis_prompt}], "Jesteś Architektem Prawdy.")
        st.markdown(f'<div style="padding:30px; border:1px solid #1E293B; font-family:serif; font-style:italic;">{final_insight}</div>', unsafe_allow_html=True)

    if st.button("ROZEDRZYJ KARTKI (RESET)"):
        st.session_state.clear()
        st.rerun()
