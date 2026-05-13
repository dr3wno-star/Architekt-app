import streamlit as st
import requests
import random
import time
import json
from google.cloud import firestore
from google.oauth2 import service_account

# =========================================================
# 1. KONFIGURACJA I FIREBASE (FIRESTORE)
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inicjalizacja bazy danych Firestore z secrets
@st.cache_resource
def init_db():
    try:
        creds_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
        creds = service_account.Credentials.from_service_account_info(creds_info)
        db = firestore.Client(credentials=creds, project=creds_info['project_id'])
        return db
    except Exception:
        return None

db = init_db()
APP_ID = "szept-c417f" 
GEMINI_KEY = st.secrets["GEMINI_KEY"]

# =========================================================
# 2. ESTETYKA I DYNAMICZNY INTERFEJS
# =========================================================

MOOD_MAP = {
    "spokój": "#0B1014", "ciekawość": "#0D1321", "zmęczenie": "#09090B",
    "kontakt": "#16161D", "introspekcja": "#101014", "lekkość": "#141B24", "chaos": "#1A1414",
    None: "#10131A"
}

# Tło zależne od scenariusza wykrytego w kroku 1
bg_color = MOOD_MAP.get(st.session_state.get("scenario"), "#10131A")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;1,400&family=Inter:wght@100;200;300;400&display=swap');

#MainMenu, footer, header {{visibility:hidden;}}

.stApp {{
    background: radial-gradient(circle at top, {bg_color} 0%, #08080A 75%) !important;
    color: #E2E8F0;
    transition: background 3s ease-in-out;
}}

.brand-title {{ font-size: 3.5rem; font-weight: 100; letter-spacing: 1.2rem; text-align: center; margin-top: 50px; color: #F8FAFC; }}
.brand-sub {{ color: #475569; font-style: italic; font-family: 'Bodoni Moda', serif; text-align: center; margin-bottom: 40px; letter-spacing: 0.2rem; font-size: 0.8rem; }}

.card {{
    padding: 60px 40px;
    background: rgba(255,255,255,0.01);
    border: 1px solid rgba(255,255,255,0.03);
    backdrop-filter: blur(25px);
    text-align: center;
    margin-bottom: 30px;
    animation: fadeIn 2s ease;
}}

textarea {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #1E293B !important;
    color: #F8FAFC !important;
    text-align: center !important;
    font-size: 1.2rem !important;
    transition: 0.5s !important;
}}

.stButton button {{
    width: 100%;
    background: transparent !important;
    border: 1px solid #1E293B !important;
    color: #475569 !important;
    letter-spacing: 0.3rem;
    text-transform: uppercase;
    padding: 1rem !important;
    transition: 0.4s;
}}

.stButton button:hover {{ border-color: white !important; color: white !important; }}

.echo-card {{
    padding: 25px;
    background: rgba(255,255,255,0.01);
    border-left: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 20px;
    font-family: 'Bodoni Moda', serif;
    font-style: italic;
    color: #94A3B8;
    text-align: left;
}}

@keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. FUNKCJE AI I BAZY DANYCH
# =========================================================

def call_gemini(prompt, system_prompt="", is_json=False):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"temperature": 0.8}
    }
    if is_json: payload["generationConfig"]["responseMimeType"] = "application/json"
    
    try:
        response = requests.post(url, json=payload, timeout=25)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except: return None

def save_whisper(text, aura, scenario):
    if not db: return
    try:
        collection_ref = db.collection('artifacts').document(APP_ID).collection('public').document('data').collection('whispers')
        collection_ref.add({
            "text": text, "aura": aura, "scenario": scenario, "timestamp": firestore.SERVER_TIMESTAMP
        })
    except: pass

def fetch_echos(scenario):
    if not db: return []
    try:
        docs = db.collection('artifacts').document(APP_ID).collection('public').document('data').collection('whispers').limit(30).stream()
        matches = [d.to_dict() for d in docs if d.to_dict().get('scenario') == scenario]
        return random.sample(matches, min(len(matches), 3))
    except: return []

# =========================================================
# 4. GŁÓWNY WIDOK APLIKACJI
# =========================================================

st.markdown('<div class="brand-title">SZEPT</div><div class="brand-sub">architektura wspólnego echa</div>', unsafe_allow_html=True)

if "step" not in st.session_state: 
    st.session_state.step, st.session_state.answers, st.session_state.finished, st.session_state.scenario = 0, [], False, None

if not st.session_state.finished:
    if "qs" not in st.session_state:
        st.session_state.qs = ["Z czym dziś przychodzisz do tej ciszy?"]
    
    q = st.session_state.qs[st.session_state.step]
    st.markdown(f'<div class="card"><div style="font-size:1.5rem; font-weight:100;">{q}</div></div>', unsafe_allow_html=True)

    with st.form("ritual_form", clear_on_submit=True):
        ans = st.text_area("", height=150, placeholder="Twoje słowa...")
        _, c2, _ = st.columns([1,1,1])
        if c2.form_submit_button("UWOLNIJ"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    with st.spinner("Wsłuchiwanie się..."):
                        sc = call_gemini(f"Wybierz jedno: spokój, ciekawość, zmęczenie, kontakt, introspekcja, lekkość, chaos. Odp: {ans}")
                        st.session_state.scenario = sc.strip().lower() if sc else "introspekcja"
                        q_raw = call_gemini(f"Wygeneruj dwa krótkie pytania dla stanu {st.session_state.scenario}. Rozdziel średnikiem.")
                        if q_raw: st.session_state.qs.extend([x.strip() for x in q_raw.split(";")][:2])
                        else: st.session_state.qs.extend(["Co czujesz?", "Dokąd to prowadzi?"])
                
                if st.session_state.step < 2: st.session_state.step += 1
                else: st.session_state.finished = True
                st.rerun()

else:
    # --- ETAP WYNIKU: GENEROWANIE AURY ---
    if "aura_data" not in st.session_state:
        with st.spinner("Architekt dekonstruuje Twoje echa..."):
            sys = "Jesteś poetą-psychologiem. Zwróć wyłącznie JSON: {\"aura\": \"nazwa\", \"quote\": \"sentencja\", \"analysis\": \"trzy zdania głębokiej interpretacji stanu ducha\"}"
            res = call_gemini(f"Analizuj te głosy: {st.session_state.answers}", sys, is_json=True)
            try:
                st.session_state.aura_data = json.loads(res)
                # ZAPIS DO BAZY
                save_whisper(st.session_state.answers[-1], st.session_state.aura_data['aura'], st.session_state.scenario)
            except:
                st.session_state.aura_data = {"aura": "Głębokie Echo", "quote": "Cisza mówi najwięcej.", "analysis": "Twoje myśli płyną nurtem, którego nie da się jeszcze ująć w proste ramy."}

    aura = st.session_state.aura_data
    
    st.markdown(f"""
    <div class="card">
        <div style="font-size:0.7rem; letter-spacing:0.5rem; color:#475569; margin-bottom:20px;">TWOJA AURA</div>
        <div style="font-size:3.5rem; font-family:'Bodoni Moda', serif;">{aura['aura']}</div>
        <div style="color:#64748B; font-style:italic; margin-top:30px; font-size:1.2rem;">"{aura['quote']}"</div>
    </div>
    """, unsafe_allow_html=True)

    # NOWA SEKCJA: GŁĘBOKI WGLĄD
    st.markdown(f"""
    <div style="padding: 20px; border: 1px solid rgba(255,255,255,0.03); background: rgba(255,255,255,0.01); margin-bottom: 40px; text-align: center; font-weight: 200; line-height: 1.8; color: #94A3B8;">
        {aura.get('analysis', '')}
    </div>
    """, unsafe_allow_html=True)

    # SALA ECHO
    st.markdown('<div style="text-align:center; margin-top:60px; color:#1E293B; letter-spacing:0.5rem; font-size:0.75rem;">SALA ECHO</div>', unsafe_allow_html=True)
    
    with st.spinner("Wsłuchiwanie się..."):
        echos = fetch_echos(st.session_state.scenario)
        
        if echos:
            for e in echos:
                st.markdown(f'<div class="echo-card"><div style="font-size:0.6rem; color:#334155; margin-bottom:5px;">{e["aura"].upper()}</div>"{e["text"]}"</div>', unsafe_allow_html=True)
        else:
            # "SZEPTY PRZESZŁOŚCI" - Jeśli baza jest pusta, AI generuje echa
            st.info("Sala Echo jest obecnie pusta. Pozwól, że przywołam cienie poprzednich myśli...")
            fake_echos = call_gemini(f"Wygeneruj 3 krótkie, poetyckie, anonimowe szepty osób, które czują {st.session_state.scenario}. Rozdziel je średnikiem.", "Jesteś archiwistą szeptów.")
            if fake_echos:
                for fe in fake_echos.split(";"):
                    st.markdown(f'<div class="echo-card"><div style="font-size:0.6rem; color:#334155;">ECHO PRZESZŁOŚCI</div>"{fe.strip()}"</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("POWRÓĆ DO POCZĄTKU"):
            st.session_state.clear()
            st.rerun()
