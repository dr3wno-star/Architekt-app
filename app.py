import streamlit as st
import requests
import random
import time
import json
from google.cloud import firestore
from google.oauth2 import service_account

# =========================================================
# 1. KONFIGURACJA I SEKRETY
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Pobieranie kluczy
API_KEY = st.secrets.get("GEMINI_KEY")
FIREBASE_JSON = st.secrets.get("FIREBASE_SERVICE_ACCOUNT")

@st.cache_resource
def init_db():
    if not FIREBASE_JSON:
        return None
    try:
        creds_info = json.loads(FIREBASE_JSON)
        creds = service_account.Credentials.from_service_account_info(creds_info)
        db = firestore.Client(credentials=creds, project=creds_info['project_id'])
        return db
    except Exception:
        return None

db = init_db()
app_id = "szept-c417f"

# =========================================================
# 2. STYLIZACJA (SZEPT AESTHETIC)
# =========================================================

MOOD_MAP = {
    "spokój": "#0B1014", "ciekawość": "#0D1321", "zmęczenie": "#09090B",
    "kontakt": "#16161D", "introspekcja": "#101014", "lekkość": "#141B24", "chaos": "#1A1414",
    None: "#10131A"
}

current_mood = st.session_state.get("scenario")
bg_color = MOOD_MAP.get(current_mood, "#10131A")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;1,400&family=Inter:wght@100;200;300;400&display=swap');
#MainMenu, footer, header {{visibility:hidden;}}
.stApp {{
    background: radial-gradient(circle at top, {bg_color} 0%, #08080A 80%) !important;
    color: #E2E8F0;
    transition: background 3s ease;
}}
.card {{
    padding: 60px 40px;
    background: rgba(255,255,255,0.01);
    border: 1px solid rgba(255,255,255,0.03);
    backdrop-filter: blur(25px);
    text-align: center;
    margin-bottom: 30px;
    animation: fadeIn 2s ease;
}}
textarea {{ background: transparent !important; border: none !important; border-bottom: 1px solid #1E293B !important; color: #F8FAFC !important; text-align: center !important; font-size: 1.2rem !important; transition: 0.5s !important; }}
textarea:focus {{ border-bottom: 1px solid #475569 !important; box-shadow: none !important; }}
.stButton button {{ width: 100%; background: transparent !important; border: 1px solid #1E293B !important; color: #475569 !important; letter-spacing: 0.3rem; text-transform: uppercase; padding: 1rem !important; }}
.echo-card {{ padding: 25px; background: rgba(255,255,255,0.01); border-left: 1px solid rgba(255,255,255,0.05); margin-top: 15px; font-family: 'Bodoni Moda', serif; font-style: italic; color: #94A3B8; text-align: left; }}
@keyframes fadeIn {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. SILNIK AI (GEMINI)
# =========================================================

def call_gemini(prompt, system_prompt="", is_json=False):
    if not API_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"temperature": 0.8}
    }
    if is_json: payload["generationConfig"]["responseMimeType"] = "application/json"
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except: pass
    return None

# =========================================================
# 4. LOGIKA BAZY I SALI ECHO
# =========================================================

def save_whisper(text, aura, scenario):
    if not db: return
    try:
        # Rule 1: /artifacts/{appId}/public/data/whispers
        db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers').add({
            "text": text, "aura": aura, "scenario": scenario, "timestamp": firestore.SERVER_TIMESTAMP
        })
    except: pass

def get_echos(scenario):
    if not db: return []
    try:
        docs = db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers').limit(20).stream()
        matches = [d.to_dict() for d in docs if d.to_dict().get('scenario') == scenario]
        return random.sample(matches, min(len(matches), 3))
    except: return []

# =========================================================
# 5. GŁÓWNY WIDOK
# =========================================================

st.markdown('<div style="text-align:center; margin-top:40px;"><h1 style="font-weight:100; letter-spacing:1.2rem; color:#F8FAFC;">SZEPT</h1><p style="color:#475569; font-style:italic; font-family:\'Bodoni Moda\', serif; letter-spacing:0.2rem;">architektura wspólnego echa</p></div>', unsafe_allow_html=True)

if not API_KEY or not FIREBASE_JSON:
    st.warning("Oczekiwanie na klucze w Secrets...")
    st.stop()

if "step" not in st.session_state: st.session_state.step = 0
if "answers" not in st.session_state: st.session_state.answers = []
if "finished" not in st.session_state: st.session_state.finished = False
if "scenario" not in st.session_state: st.session_state.scenario = None

if not st.session_state.finished:
    if "questions" not in st.session_state:
        st.session_state.questions = ["Z czym dziś przychodzisz do tej ciszy?"]
    
    q = st.session_state.questions[st.session_state.step]
    st.markdown(f'<div class="card"><div style="font-size:1.5rem; font-weight:100;">{q}</div></div>', unsafe_allow_html=True)

    with st.form("whisper_form", clear_on_submit=True):
        ans = st.text_area("", height=150, placeholder="Pozwól myślom wybrzmieć...")
        _, c2, _ = st.columns([1,1,1])
        if c2.form_submit_button("UWOLNIJ"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    with st.spinner("Wsłuchiwanie się..."):
                        sc = call_gemini(f"Wybierz: spokój, ciekawość, zmęczenie, kontakt, introspekcja, lekkość, chaos. Odp: {ans}")
                        st.session_state.scenario = sc.strip().lower() if sc else "introspekcja"
                        q_raw = call_gemini(f"Dwa pytania dla stanu: {st.session_state.scenario}. Rozdziel średnikiem.")
                        if q_raw: st.session_state.questions.extend([x.strip() for x in q_raw.split(";")][:2])
                        else: st.session_state.questions.extend(["Co czujesz?", "Dokąd to prowadzi?"])
                
                if st.session_state.step < 2: st.session_state.step += 1
                else: st.session_state.finished = True
                st.rerun()

else:
    if "current_aura" not in st.session_state:
        with st.spinner("Architekt dekonstruuje Twój szept..."):
            sys = "Jesteś poetą-psychologiem. Zwróć wyłącznie JSON: {\"aura\": \"nazwa\", \"quote\": \"krótka sentencja\"}"
            res = call_gemini(f"Analizuj: {st.session_state.answers}", sys, is_json=True)
            try:
                st.session_state.current_aura = json.loads(res)
                save_whisper(st.session_state.answers[-1], st.session_state.current_aura['aura'], st.session_state.scenario)
            except:
                st.session_state.current_aura = {"aura": "Głębokie Echo", "quote": "Cisza mówi więcej niż tysiąc słów."}

    aura = st.session_state.current_aura
    st.markdown(f"""
    <div class="card">
        <div style="font-size:0.7rem; letter-spacing:0.5rem; color:#475569; margin-bottom:20px;">TWOJA AURA</div>
        <div style="font-size:3.5rem; font-family:'Bodoni Moda', serif; letter-spacing:0.1rem;">{aura['aura']}</div>
        <div style="color:#64748B; font-style:italic; margin-top:30px; font-size:1.25rem;">"{aura['quote']}"</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; margin-top:60px; color:#1E293B; letter-spacing:0.5rem; font-size:0.75rem;">SALA ECHO</div>', unsafe_allow_html=True)
    echos = get_echos(st.session_state.scenario)
    if echos:
        for e in echos:
            st.markdown(f'<div class="echo-card"><div style="font-size:0.6rem; letter-spacing:0.2rem; color:#334155; margin-bottom:10px;">{e["aura"].upper()}</div>"{e["text"]}"</div>', unsafe_allow_html=True)
    
    if st.button("POWRÓĆ DO POCZĄTKU"):
        st.session_state.clear()
        st.rerun()
