import streamlit as st
import requests
import json
import time

# =========================================================
# 1. KONFIGURACJA
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
        "generationConfig": {"temperature": 1.0} # Wyższa temperatura dla unikalności
    }
    try:
        r = requests.post(url, json=payload, timeout=25)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except: return "Atrament zastyga w bezruchu..."

# =========================================================
# 2. ESTETYKA
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@200;400&display=swap');
#MainMenu, footer, header {visibility:hidden;}
.stApp { background: #0A0A0C !important; color: #D1D5DB; }
.journal-page {
    border-left: 1px solid rgba(255,255,255,0.05);
    padding-left: 30px;
    margin-top: 50px;
    font-family: 'Inter', sans-serif;
}
.user-text { color: #8892B0; font-style: italic; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 5px; }
.ai-text { 
    color: #F8FAFC; 
    font-family: 'Bodoni Moda', serif; 
    font-size: 1.25rem; 
    margin-bottom: 45px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOGIKA DZIENNIKA (INTERAKCJA)
# =========================================================

if "journal" not in st.session_state:
    st.session_state.journal = []
    st.session_state.finished = False
    
    # DZIENNIK ZADAJE PIERWSZE PYTANIE
    with st.spinner("Dziennik otwiera się..."):
        sys_init = "Jesteś świadomym, tajemniczym Dziennikiem. Twoim zadaniem jest przywitać nowego użytkownika jednym, niezwykle przenikliwym i nieoczekiwanym pytaniem. Nie pytaj o dzień ani emocje wprost. Zapytaj o detal, o cień, o coś, co użytkownik wolałby pominąć. Maksymalnie 2 krótkie zdania."
        first_move = call_ai([{"role": "user", "content": "Otwórz się i przywitaj mnie."}], sys_init)
        st.session_state.journal.append({"role": "assistant", "content": first_move})

st.markdown('<h1 style="font-weight:100; letter-spacing:1.2rem; text-align:center; margin-bottom:0;">SZEPT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#334155; font-size:0.7rem; letter-spacing:0.3rem; margin-bottom:50px;">INTERAKTYWNY ARTEFAKT</p>', unsafe_allow_html=True)

# Wyświetlanie wpisów
journal_container = st.container()
with journal_container:
    st.markdown('<div class="journal-page">', unsafe_allow_html=True)
    for m in st.session_state.journal:
        if m["role"] == "user":
            st.markdown(f'<div class="user-text">{m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-text">{m["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Interfejs wprowadzania danych
if not st.session_state.finished:
    with st.form("input_form", clear_on_submit=True):
        user_input = st.text_area("", placeholder="Odpowiedz atramentem...", height=100)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c3:
            submit = st.form_submit_button("ODDAJ SŁOWA")
        with c2:
            finish = st.form_submit_button("ZAMKNIJ")

    if submit and user_input.strip():
        st.session_state.journal.append({"role": "user", "content": user_input})
        
        sys_prompt = "Jesteś Dziennikiem. Reaguj na słowa użytkownika. Bądź inteligentny, nieco prowokujący, dostrzegaj to, co ukryte między wierszami. Odpowiadaj krótko (1-3 zdania). Prowadź dialog, nie ankietę."
        
        with st.spinner("Wchłanianie..."):
            response = call_ai(st.secrets.get("journal", st.session_state.journal), sys_prompt)
            st.session_state.journal.append({"role": "assistant", "content": response})
        st.rerun()

    if finish:
        st.session_state.finished = True
        st.rerun()

else:
    # PODSUMOWANIE DZIENNIKA
    st.markdown("---")
    with st.spinner("Dziennik analizuje Twój ślad..."):
        analysis_prompt = f"Na podstawie tej rozmowy: {st.session_state.journal}. Podsumuj naszą interakcję. Co dziś w Tobie przeczytałem? Opisz to jako Architekt dusz, unikając banałów."
        final_insight = call_ai([{"role": "user", "content": analysis_prompt}], "Jesteś surowym obserwatorem prawdy.")
        
        st.markdown(f'<div style="padding:40px; border:1px solid #1E293B; font-family:serif; font-style:italic; font-size:1.1rem; line-height:1.8;">{final_insight}</div>', unsafe_allow_html=True)

    if st.button("SPAL DZIENNIK (RESET)"):
        st.session_state.clear()
        st.rerun()
