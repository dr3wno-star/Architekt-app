import streamlit as st
import requests
import random
import time
import json
from google.cloud import firestore
from google.oauth2 import service_account

# =========================================================
# 1. KONFIGURACJA I FIREBASE
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def init_db():
    try:
        creds_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
        creds = service_account.Credentials.from_service_account_info(creds_info)
        db = firestore.Client(credentials=creds, project=creds_info['project_id'])
        return db
    except:
        return None

db = init_db()
app_id = "szept-c417f" 
API_KEY = st.secrets.get("GEMINI_KEY", "")

# =========================================================
# 2. SILNIK AI (POPRAWIONA KOMUNIKACJA)
# =========================================================

def call_gemini(prompt, system_prompt="", is_json=False):
    if not API_KEY:
        return None
    
    # Używamy modelu zalecanego w dokumentacji środowiska
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "topK": 40,
            "maxOutputTokens": 1024,
        }
    }
    
    if is_json:
        payload["generationConfig"]["responseMimeType"] = "application/json"

    for delay in [1, 2, 4]:
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                return text
        except:
            time.sleep(delay)
    return None

# =========================================================
# 3. LOGIKA I STYLE
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
    transition: background 3s ease;
}}
.question-card {{
    padding: 60px 40px;
    background: rgba(255,255,255,0.01);
    border: 1px solid rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    margin-bottom: 30px;
    text-align: center;
}}
.aura-box {{
    padding: 60px 30px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    background: rgba(255,255,255,0.01);
    margin-top: 20px;
}}
textarea {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #1E293B !important;
    color: #F8FAFC !important;
    text-align: center !important;
    font-size: 1.1rem !important;
}}
.stButton button {{
    width: 100%;
    background: transparent !important;
    border: 1px solid #1E293B !important;
    color: #475569 !important;
    letter-spacing: 0.3rem;
    text-transform: uppercase;
}}
.echo-card {{
    padding: 20px;
    background: rgba(255,255,255,0.02);
    border-left: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 15px;
    font-family: 'Bodoni Moda', serif;
    font-style: italic;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 4. FUNKCJE POMOCNICZE BAZY
# =========================================================

def save_to_db(text, aura, scenario):
    if not db: return
    try:
        db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers').add({
            "text": text, "aura": aura, "scenario": scenario, "timestamp": firestore.SERVER_TIMESTAMP
        })
    except: pass

def get_from_db(scenario):
    if not db: return []
    try:
        docs = db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers').stream()
        matches = [d.to_dict() for d in docs if d.to_dict().get('scenario') == scenario]
        return random.sample(matches, min(len(matches), 3))
    except: return []

# =========================================================
# 5. PRZEBIEG RYTUAŁU
# =========================================================

if "step" not in st.session_state: st.session_state.step = 0
if "answers" not in st.session_state: st.session_state.answers = []
if "finished" not in st.session_state: st.session_state.finished = False
if "scenario" not in st.session_state: st.session_state.scenario = None

st.markdown('<div style="text-align:center; margin-top:40px;"><h1 style="font-weight:100; letter-spacing:1rem;">SZEPT</h1><p style="color:#475569; font-style:italic; font-family:\'Bodoni Moda\', serif;">sala wspólnego echa</p></div>', unsafe_allow_html=True)

if not st.session_state.finished:
    if "questions" not in st.session_state:
        st.session_state.questions = ["Z czym dziś przychodzisz do tej ciszy?"]
    
    q = st.session_state.questions[st.session_state.step]
    st.markdown(f'<div class="question-card"><div style="font-size:1.3rem; font-weight:200;">{q}</div></div>', unsafe_allow_html=True)

    with st.form("whisper_form", clear_on_submit=True):
        ans = st.text_area("", height=150, placeholder="Twoje słowa...")
        _, c2, _ = st.columns([1,1,1])
        if c2.form_submit_button("UWOLNIJ SZEPT"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    with st.spinner("Wsłuchiwanie się..."):
                        sc = call_gemini(f"Wybierz jedno słowo: spokój, ciekawość, zmęczenie, kontakt, introspekcja, lekkość, chaos. Odpowiedź użytkownika: {ans}")
                        st.session_state.scenario = sc.strip().lower() if sc else "introspekcja"
                        q_raw = call_gemini(f"Wygeneruj dwa krótkie pytania dla stanu: {st.session_state.scenario}. Rozdziel je średnikiem.")
                        if q_raw:
                            st.session_state.questions.extend([x.strip() for x in q_raw.split(";")][:2])
                        else:
                            st.session_state.questions.extend(["Co czujesz teraz?", "Dokąd prowadzi ta myśl?"])
                
                if st.session_state.step < 2:
                    st.session_state.step += 1
                else:
                    st.session_state.finished = True
                st.rerun()

else:
    # ANALIZA KOŃCOWA
    if "current_aura" not in st.session_state:
        with st.spinner("Architekt dekonstruuje Twój szept..."):
            sys_prompt = "Jesteś poetą. Zwróć wyłącznie JSON: {\"aura\": \"nazwa\", \"quote\": \"sentencja\"}"
            user_prompt = f"Analizuj te głosy: {st.session_state.answers}"
            res_text = call_gemini(user_prompt, sys_prompt, is_json=True)
            try:
                st.session_state.current_aura = json.loads(res_text)
                save_to_db(st.session_state.answers[-1], st.session_state.current_aura['aura'], st.session_state.scenario)
            except:
                st.session_state.current_aura = {"aura": "Nienazwane Echo", "quote": "Cisza mówi najwięcej."}

    aura = st.session_state.current_aura
    st.markdown(f"""
    <div class="aura-box">
        <div style="font-size:0.6rem; letter-spacing:0.4rem; color:#475569;">TWOJA AURA</div>
        <div style="font-size:3rem; font-family:'Bodoni Moda', serif;">{aura['aura']}</div>
        <div style="color:#64748B; font-style:italic; margin-top:20px;">"{aura['quote']}"</div>
    </div>
    """, unsafe_allow_html=True)

    # SALA ECHO
    st.markdown('<div style="text-align:center; margin-top:50px; font-size:0.7rem; letter-spacing:0.4rem;">SALA ECHO</div>', unsafe_allow_html=True)
    echos = get_from_db(st.session_state.scenario)
    if echos:
        for e in echos:
            st.markdown(f'<div class="echo-card"><div style="font-size:0.6rem; color:#334155;">{e["aura"].upper()}</div>"{e["text"]}"</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center; color:#334155; margin-top:20px;">Cisza... Jesteś tu pierwszy.</div>', unsafe_allow_html=True)

    if st.button("POWRÓĆ DO POCZĄTKU"):
        st.session_state.clear()
        st.rerun()
