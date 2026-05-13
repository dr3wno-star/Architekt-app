```python
import streamlit as st
import requests
import random
import time
import json
from google.cloud import firestore
from google.oauth2 import service_account

# =========================================================
# KONFIGURACJA I FIREBASE (DATABASE)
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inicjalizacja Firestore (Zgodnie z Rule 1 & 3)
# Zakładamy, że __firebase_config jest w st.secrets
def init_db():
    try:
        # Przykładowa konfiguracja dla Streamlit Cloud / Secrets
        # Wymaga ustawienia klucza serwisowego w secrets
        creds_dict = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        db = firestore.Client(credentials=creds, project=creds_dict['project_id'])
        return db
    except:
        return None

db = init_db()
app_id = "szept-v2"
API_KEY = st.secrets.get("GEMINI_KEY", "")

# =========================================================
# STYLIZACJA (SZEPT AESTHETIC)
# =========================================================

def inject_ui(mood_color="#10131A"):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;1,400&family=Inter:wght@100;200;300;400&display=swap');

    #MainMenu, footer, header {{visibility:hidden;}}

    .stApp {{
        background: radial-gradient(circle at top, {mood_color} 0%, #08080A 65%) !important;
        color: #E2E8F0;
        transition: background 3s ease;
    }}

    .brand {{ text-align: center; margin-top: 40px; margin-bottom: 40px; }}
    .brand-title {{ font-size: 3.5rem; font-weight: 100; letter-spacing: 1.2rem; color: #F8FAFC; }}
    .brand-sub {{ color: #475569; font-style: italic; font-family: 'Bodoni Moda', serif; letter-spacing: 0.2rem; font-size: 0.8rem; }}

    .question-card {{
        padding: 40px;
        background: rgba(255,255,255,0.01);
        border: 1px solid rgba(255,255,255,0.03);
        backdrop-filter: blur(15px);
        margin-bottom: 30px;
        text-align: center;
    }}

    .aura-box {{
        padding: 60px 30px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        background: rgba(255,255,255,0.01);
        margin-bottom: 40px;
        animation: fadeIn 2s ease;
    }}

    .echo-container {{
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }}

    .echo-card {{
        padding: 20px;
        background: rgba(255,255,255,0.02);
        margin-bottom: 15px;
        border-left: 1px solid #1E293B;
        font-family: 'Bodoni Moda', serif;
        font-style: italic;
        color: #94A3B8;
        font-size: 0.95rem;
    }}

    .echo-aura {{
        font-size: 0.65rem;
        letter-spacing: 0.2rem;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}

    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# KOMUNIKACJA AI
# =========================================================

def call_gemini(prompt, system_prompt=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"responseMimeType": "application/json" if "JSON" in system_prompt else "text/plain"}
    }
    try:
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except: return None
    return None

# =========================================================
# OPERACJE NA DANYCH (SALA ECHO)
# =========================================================

def save_whisper(whisper_text, aura_data, scenario):
    if not db: return
    # Rule 1: /artifacts/{appId}/public/data/{collectionName}
    collection_ref = db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers')
    collection_ref.add({
        "whisper": whisper_text,
        "aura": aura_data['aura'],
        "scenario": scenario,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def get_echos(scenario):
    if not db: return []
    # Rule 2: Fetch all and filter in memory to avoid complex queries
    collection_ref = db.collection('artifacts').document(app_id).collection('public').document('data').collection('whispers')
    docs = collection_ref.stream()
    
    all_whispers = []
    for d in docs:
        data = d.to_dict()
        if data.get('scenario') == scenario:
            all_whispers.append(data)
    
    # Zwróć 3 losowe z tego samego scenariusza
    if len(all_whispers) > 3:
        return random.sample(all_whispers, 3)
    return all_whispers

# =========================================================
# GŁÓWNY FLOW
# =========================================================

if "step" not in st.session_state: st.session_state.step = 0
if "answers" not in st.session_state: st.session_state.answers = []
if "finished" not in st.session_state: st.session_state.finished = False
if "scenario" not in st.session_state: st.session_state.scenario = None

MOOD_MAP = {"spokój": "#0B1014", "ciekawość": "#0D1321", "zmęczenie": "#09090B", "kontakt": "#16161D", "introspekcja": "#101014", "lekkość": "#141B24", "chaos": "#1A1414"}
inject_ui(MOOD_MAP.get(st.session_state.scenario, "#10131A"))

st.markdown('<div class="brand"><div class="brand-title">SZEPT</div><div class="brand-sub">sala wspólnego echa</div></div>', unsafe_allow_html=True)

if not st.session_state.finished:
    # (Logika pytań pozostaje taka sama jak w poprzedniej wersji)
    if "questions" not in st.session_state:
        st.session_state.questions = [random.choice(["Z czym dziś przychodzisz?", "Co dominuje w Twojej ciszy?", "Jakie słowo Cię dziś prowadzi?"])]
    
    q = st.session_state.questions[st.session_state.step]
    st.markdown(f'<div class="question-card"><div style="font-size:1.3rem; font-weight:200;">{q}</div></div>', unsafe_allow_html=True)

    with st.form("ritual"):
        ans = st.text_area("", height=150, placeholder="Twoje słowa...")
        _, c2, _ = st.columns([1,1,1])
        if c2.form_submit_button("UWOLNIJ"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    scenario = call_gemini(f"Wybierz: spokój, ciekawość, zmęczenie, kontakt, introspekcja, lekkość, chaos. Odpowiedź: {ans}")
                    st.session_state.scenario = scenario.strip().lower() if scenario else "introspekcja"
                    q_raw = call_gemini(f"Dwa pytania dla stanu: {st.session_state.scenario}. Rozdziel średnikiem.")
                    st.session_state.questions.extend([x.strip() for x in q_raw.split(";")][:2] if q_raw else ["Co czujesz?", "Dokąd zmierzasz?"])
                
                if st.session_state.step < 2: st.session_state.step += 1
                else: st.session_state.finished = True
                st.rerun()

else:
    # ETAP WYNIKU I SALI ECHO
    if "current_aura" not in st.session_state:
        with st.spinner("Splatanie echa..."):
            system_p = 'Zwróć JSON: {"aura": "nazwa", "desc": "zdanie", "traits": [], "quote": "cytat"}'
            user_p = f"Analiza: {st.session_state.answers}"
            res = call_gemini(user_p, system_p)
            try:
                st.session_state.current_aura = json.loads(res)
                # ZAPIS DO BAZY (Sala Echo)
                save_whisper(st.session_state.answers[-1], st.session_state.current_aura, st.session_state.scenario)
            except:
                st.session_state.current_aura = {"aura": "Bez imienia", "desc": "Nienazwana obecność.", "traits": ["cisza"], "quote": "..."}

    aura = st.session_state.current_aura
    
    # Wyświetlenie Aury
    st.markdown(f"""
    <div class="aura-box">
        <div style="font-size:0.6rem; letter-spacing:0.4rem; color:#475569;">TWOJA AURA</div>
        <div style="font-size:3.2rem; font-family:'Bodoni Moda', serif;">{aura['aura']}</div>
        <div style="color:#64748B; font-style:italic;">"{aura['quote']}"</div>
    </div>
    """, unsafe_allow_html=True)

    # SALA ECHO - Połączenie z innymi
    st.markdown('<div class="history-label" style="text-align:center; margin-top:40px;">SALA ECHO</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-size:0.8rem; color:#475569; margin-bottom:20px;">Inni, którzy dzielą Twój kierunek:</div>', unsafe_allow_html=True)
    
    echos = get_echos(st.session_state.scenario)
    
    if echos:
        for echo in echos:
            st.markdown(f"""
            <div class="echo-card">
                <div class="echo-aura">{echo['aura']}</div>
                "{echo['whisper']}"
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center; font-style:italic; color:#334155;">Na razie panuje tu cisza...</div>', unsafe_allow_html=True)

    if st.button("POWRÓĆ DO CISZY"):
        st.session_state.clear()
        st.rerun()

```
    
