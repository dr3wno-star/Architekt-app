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
        # Parsowanie danych konta serwisowego z secrets
        creds_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
        creds = service_account.Credentials.from_service_account_info(creds_info)
        db = firestore.Client(credentials=creds, project=creds_info['project_id'])
        return db
    except Exception as e:
        # Jeśli baza nie jest podłączona, aplikacja zadziała w trybie lokalnym
        return None

db = init_db()
# ID Twojego projektu Firestore: szept-c417f
app_id = "szept-c417f" 
API_KEY = st.secrets.get("GEMINI_KEY", "")

# =========================================================
# 2. INTERFEJS I STYLIZACJA (DYNAMICZNE TŁO)
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
    background: radial-gradient(circle at top, {bg_color} 0%, #08080A 75%) !important;
    color: #E2E8F0;
    transition: background 3s ease-in-out;
}}

.brand {{ text-align: center; margin-top: 40px; margin-bottom: 40px; }}
.brand-title {{ font-size: 3.5rem; font-weight: 100; letter-spacing: 1.2rem; color: #F8FAFC; animation: fadeIn 2s ease; }}
.brand-sub {{ color: #475569; font-style: italic; font-family: 'Bodoni Moda', serif; letter-spacing: 0.2rem; font-size: 0.8rem; margin-top:10px; }}

.question-card {{
    padding: 60px 40px;
    background: rgba(255,255,255,0.01);
    border: 1px solid rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    margin-bottom: 30px;
    text-align: center;
    animation: slideUp 1.5s ease;
}}

.aura-box {{
    padding: 80px 40px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    background: rgba(255,255,255,0.015);
    margin-top: 30px;
    animation: fadeIn 3s ease;
}}

.echo-card {{
    padding: 25px;
    background: rgba(255,255,255,0.01);
    border-left: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 20px;
    font-family: 'Bodoni Moda', serif;
    font-style: italic;
    color: #94A3B8;
    line-height: 1.6;
}}

@keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
@keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}

textarea {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #1E293B !important;
    color: #F8FAFC !important;
    text-align: center !important;
    font-size: 1.1rem !important;
    transition: 0.5s !important;
}}

.stButton button {{
    width: 100%;
    background: transparent !important;
    border: 1px solid #1E293B !important;
    color: #475569 !important;
    padding: 1rem !important;
    border-radius: 0px !important;
    letter-spacing: 0.3rem;
    transition: 0.4s;
    text-transform: uppercase;
    font-size: 0.75rem;
}}

.stButton button:hover {{
    border-color: #F8FAFC !important;
    color: white !important;
}}
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
        "generationConfig": {"responseMimeType": "application/json" if is_json else "text/plain"}
    }
    for delay in [1, 2, 4]:
        try:
            response = requests.post(url, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        except: time.sleep(delay)
    return None

# =========================================================
# 4. LOGIKA SALI ECHO (PERSYSTENCJA DANYCH)
# =========================================================

def save_whisper(text, aura_name, scenario):
    if not db: return
    try:
        # Path: /artifacts/{app_id}/public/data/whispers
        collection_ref = db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers')
        collection_ref.add({
            "text": text,
            "aura": aura_name,
            "scenario": scenario,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
    except Exception: pass

def fetch_echos(scenario):
    if not db: return []
    try:
        # Pobieramy dokumenty z pasującym scenariuszem
        docs = db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers').stream()
        results = [d.to_dict() for d in docs if d.to_dict().get('scenario') == scenario]
        # Zwracamy maksymalnie 3 losowe szepty
        return random.sample(results, min(len(results), 3))
    except Exception: return []

# =========================================================
# 5. GŁÓWNY FLOW APLIKACJI
# =========================================================

if "step" not in st.session_state: st.session_state.step = 0
if "answers" not in st.session_state: st.session_state.answers = []
if "finished" not in st.session_state: st.session_state.finished = False
if "scenario" not in st.session_state: st.session_state.scenario = None

st.markdown('<div class="brand"><div class="brand-title">SZEPT</div><div class="brand-sub">architektura wspólnego echa</div></div>', unsafe_allow_html=True)

if not st.session_state.finished:
    if "questions" not in st.session_state:
        st.session_state.questions = [random.choice([
            "Z czym dziś przychodzisz do tej ciszy?",
            "Co dominuje w Twoich myślach w tej chwili?",
            "Jakie jedno słowo najlepiej opisuje Twój dzień?"
        ])]
    
    q = st.session_state.questions[st.session_state.step]
    st.markdown(f'<div class="question-card"><div style="font-size:1.4rem; font-weight:100; letter-spacing:0.05rem;">{q}</div></div>', unsafe_allow_html=True)

    with st.form("ritual_form", clear_on_submit=True):
        ans = st.text_area("", height=150, placeholder="Twoje słowa mają znaczenie...")
        _, c2, _ = st.columns([1,1,1])
        if c2.form_submit_button("UWOLNIJ SZEPT"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    with st.spinner("Analiza tonu..."):
                        sc = call_gemini(f"Wybierz jedno: spokój, ciekawość, zmęczenie, kontakt, introspekcja, lekkość, chaos. Odpowiedź: {ans}")
                        st.session_state.scenario = sc.strip().lower() if sc else "introspekcja"
                        # Generowanie pytań na żywo pod scenariusz
                        q_raw = call_gemini(f"Wygeneruj dwa krótkie, głębokie pytania dla osoby w stanie: {st.session_state.scenario}. Rozdziel średnikiem.")
                        if q_raw:
                            st.session_state.questions.extend([x.strip() for x in q_raw.split(";")][:2])
                        else:
                            st.session_state.questions.extend(["Co czujesz w głębi?", "Dokąd prowadzi Cię ta myśl?"])
                
                if st.session_state.step < 2: 
                    st.session_state.step += 1
                else: 
                    st.session_state.finished = True
                st.rerun()

else:
    # --- ETAP WYNIKU I SALI ECHO ---
    if "current_aura" not in st.session_state:
        with st.spinner("Splatanie Twojego echa..."):
            system = 'Zwróć JSON: {"aura": "poetycka nazwa", "quote": "mistyczna sentencja"}'
            user = f"Analizuj rytuał: {st.session_state.answers}"
            res = call_gemini(user, system, is_json=True)
            try:
                st.session_state.current_aura = json.loads(res)
                # Zapis do bazy danych
                save_whisper(st.session_state.answers[-1], st.session_state.current_aura['aura'], st.session_state.scenario)
            except:
                st.session_state.current_aura = {"aura": "Nienazwane Echo", "quote": "Cisza jest najgłębszą z odpowiedzi."}

    aura = st.session_state.current_aura
    
    st.markdown(f"""
    <div class="aura-box">
        <div style="font-size:0.6rem; letter-spacing:0.5rem; color:#475569; margin-bottom:20px;">TWOJA AURA</div>
        <div style="font-size:3.5rem; font-family:'Bodoni Moda', serif; letter-spacing:0.1rem;">{aura['aura']}</div>
        <div style="color:#64748B; font-style:italic; margin-top:30px; font-size:1.2rem;">"{aura['quote']}"</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; margin-top:80px; color:#1E293B; letter-spacing:0.5rem; font-size:0.7rem;">SALA ECHO</div>', unsafe_allow_html=True)
    
    with st.spinner("Wsłuchiwanie się w głosy innych..."):
        echos = fetch_echos(st.session_state.scenario)
        if echos:
            for e in echos:
                st.markdown(f"""
                <div class="echo-card">
                    <div style="font-size:0.6rem; letter-spacing:0.2rem; color:#334155; margin-bottom:5px;">{e["aura"].upper()}</div>
                    "{e["text"]}"
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center; margin-top:20px; font-style:italic; color:#334155;">Na razie panuje tu cisza. Jesteś pierwszym echem w tym nastroju.</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("POWRÓĆ DO POCZĄTKU"):
        st.session_state.clear()
        st.rerun()
