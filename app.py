import streamlit as st
import requests
import random
import time
import json
from google.cloud import firestore
from google.oauth2 import service_account

# =========================================================
# 1. KONFIGURACJA I POBIERANIE SEKRETÓW
# =========================================================

st.set_page_config(page_title="SZEPT", page_icon="🌙", layout="centered")

# Bezpieczne pobieranie kluczy
def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return None

GEMINI_KEY = get_secret("GEMINI_KEY")
FIREBASE_JSON = get_secret("FIREBASE_SERVICE_ACCOUNT")

# Inicjalizacja Firestore
@st.cache_resource
def init_db():
    if not FIREBASE_JSON: return None
    try:
        creds_info = json.loads(FIREBASE_JSON)
        creds = service_account.Credentials.from_service_account_info(creds_info)
        return firestore.Client(credentials=creds, project=creds_info['project_id'])
    except: return None

db = init_db()
APP_ID = "szept-c417f"

# =========================================================
# 2. STYLIZACJA (SZEPT AESTHETIC)
# =========================================================

MOOD_COLORS = {
    "spokój": "#0B1014", "ciekawość": "#0D1321", "zmęczenie": "#09090B",
    "kontakt": "#16161D", "introspekcja": "#101014", "lekkość": "#141B24", "chaos": "#1A1414",
    None: "#10131A"
}

bg_color = MOOD_COLORS.get(st.session_state.get("scenario"), "#10131A")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;1,400&family=Inter:wght@100;200;300;400&display=swap');
#MainMenu, footer, header {{visibility:hidden;}}
.stApp {{ background: radial-gradient(circle at top, {bg_color} 0%, #08080A 80%) !important; color: #E2E8F0; transition: background 3s ease; }}
.card {{ padding: 60px 40px; background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); backdrop-filter: blur(25px); text-align: center; margin-bottom: 30px; }}
textarea {{ background: transparent !important; border: none !important; border-bottom: 1px solid #1E293B !important; color: #F8FAFC !important; text-align: center !important; font-size: 1.2rem !important; }}
.stButton button {{ width: 100%; background: transparent !important; border: 1px solid #1E293B !important; color: #475569 !important; letter-spacing: 0.3rem; padding: 1rem !important; }}
.echo-card {{ padding: 25px; background: rgba(255,255,255,0.01); border-left: 1px solid rgba(255,255,255,0.05); margin-top: 15px; font-family: 'Bodoni Moda', serif; font-style: italic; color: #94A3B8; text-align: left; }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. SILNIK I WIDOK
# =========================================================

st.markdown('<div style="text-align:center; margin-top:40px;"><h1 style="font-weight:100; letter-spacing:1.2rem;">SZEPT</h1></div>', unsafe_allow_html=True)

# Diagnostyka widoczna dla Ciebie w aplikacji
if not GEMINI_KEY or not FIREBASE_JSON:
    st.error("⚠️ SYSTEM NIEAKTYWNY: Brak kluczy w Secrets.")
    st.info("Wejdź w Settings -> Secrets w Streamlit Cloud i wklej klucze.")
    st.stop()

def call_ai(prompt, sys="", is_json=False):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "systemInstruction": {"parts": [{"text": sys}]}, "generationConfig": {"temperature": 0.8}}
    if is_json: payload["generationConfig"]["responseMimeType"] = "application/json"
    try:
        r = requests.post(url, json=payload, timeout=25)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except: return None

# --- FLOW ---
if "step" not in st.session_state: st.session_state.step, st.session_state.answers, st.session_state.finished, st.session_state.scenario = 0, [], False, None

if not st.session_state.finished:
    if "qs" not in st.session_state: st.session_state.qs = ["Z czym przychodzisz dziś do tej ciszy?"]
    st.markdown(f'<div class="card"><div style="font-size:1.5rem; font-weight:100;">{st.session_state.qs[st.session_state.step]}</div></div>', unsafe_allow_html=True)
    with st.form("f"):
        ans = st.text_area("", height=150)
        if st.form_submit_button("UWOLNIJ"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    with st.spinner("Wsłuchiwanie..."):
                        sc = call_ai(f"Wybierz: spokój, ciekawość, zmęczenie, kontakt, introspekcja, lekkość, chaos. Odp: {ans}")
                        st.session_state.scenario = sc.strip().lower() if sc else "introspekcja"
                        q_raw = call_ai(f"Dwa pytania dla stanu {st.session_state.scenario}. Rozdziel średnikiem.")
                        st.session_state.qs.extend([x.strip() for x in q_raw.split(";")][:2] if q_raw else ["Co czujesz?", "Dokąd to prowadzi?"])
                if st.session_state.step < 2: st.session_state.step += 1
                else: st.session_state.finished = True
                st.rerun()
else:
    if "aura" not in st.session_state:
        with st.spinner("Splatanie echa..."):
            res = call_ai(f"Analizuj: {st.session_state.answers}", "Zwróć JSON: {\"aura\": \"nazwa\", \"quote\": \"sentencja\"}", True)
            try: st.session_state.aura = json.loads(res)
            except: st.session_state.aura = {"aura": "Głębokie Echo", "quote": "Cisza jest Twoim sprzymierzeńcem."}
            if db:
                db.collection('artifacts').document(APP_ID).collection('public').document('data').collection('whispers').add({
                    "text": st.session_state.answers[-1], "aura": st.session_state.aura['aura'], "scenario": st.session_state.scenario, "timestamp": firestore.SERVER_TIMESTAMP
                })

    a = st.session_state.aura
    st.markdown(f'<div class="card"><div style="font-size:0.7rem; letter-spacing:0.5rem; color:#475569;">AURA</div><div style="font-size:3.5rem; font-family:Bodoni Moda;">{a["aura"]}</div><div style="font-style:italic; margin-top:30px;">"{a["quote"]}"</div></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size:0.7rem; letter-spacing:0.4rem;">SALA ECHO</p>', unsafe_allow_html=True)
    if db:
        docs = db.collection('artifacts').document(APP_ID).collection('public').document('data').collection('whispers').limit(20).stream()
        matches = [d.to_dict() for d in docs if d.to_dict().get('scenario') == st.session_state.scenario]
        for e in random.sample(matches, min(len(matches), 3)):
            st.markdown(f'<div class="echo-card"><div style="font-size:0.6rem;">{e["aura"].upper()}</div>"{e["text"]}"</div>', unsafe_allow_html=True)
    if st.button("RESET"):
        st.session_state.clear()
        st.rerun()
        
