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

st.set_page_config(page_title="SZEPT", page_icon="🌙", layout="centered")

@st.cache_resource
def init_db():
    try:
        creds_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
        creds = service_account.Credentials.from_service_account_info(creds_info)
        return firestore.Client(credentials=creds, project=creds_info['project_id'])
    except:
        return None

db = init_db()
APP_ID = "szept-c417f"
GEMINI_KEY = st.secrets.get("GEMINI_KEY")

# =========================================================
# 2. SILNIK AI (DYNAMIKA I RETRY)
# =========================================================

def call_gemini(prompt, system_prompt="", is_json=False):
    if not GEMINI_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.9, 
            "responseMimeType": "application/json" if is_json else "text/plain"
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=25)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except: return None

# =========================================================
# 3. STYLE I ESTETYKA
# =========================================================

def apply_styles(hex_color="#10131A"):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;1,400&family=Inter:wght@100;200;300;400&display=swap');
    #MainMenu, footer, header {{visibility:hidden;}}
    .stApp {{
        background: radial-gradient(circle at top, {hex_color}44 0%, #08080A 80%) !important;
        color: #E2E8F0;
        transition: background 3s ease;
    }}
    .brand-title {{ font-size: 3.5rem; font-weight: 100; letter-spacing: 1.2rem; text-align: center; margin-top: 50px; color: #F8FAFC; }}
    .brand-sub {{ color: #475569; font-style: italic; font-family: 'Bodoni Moda', serif; text-align: center; margin-bottom: 40px; font-size: 0.8rem; letter-spacing: 0.2rem; }}
    .card {{
        padding: 50px 40px;
        background: rgba(255,255,255,0.01);
        border: 1px solid rgba(255,255,255,0.03);
        backdrop-filter: blur(25px);
        text-align: center;
        margin-bottom: 30px;
    }}
    textarea {{ background: transparent !important; border: none !important; border-bottom: 1px solid #1E293B !important; color: #F8FAFC !important; text-align: center !important; font-size: 1.2rem !important; }}
    .stButton button {{ width: 100%; background: transparent !important; border: 1px solid #1E293B !important; color: #475569 !important; letter-spacing: 0.3rem; text-transform: uppercase; padding: 15px !important; transition: 0.4s; }}
    .stButton button:hover {{ border-color: white !important; color: white !important; }}
    .echo-card {{ padding: 25px; background: rgba(255,255,255,0.01); border-left: 1px solid rgba(255,255,255,0.05); margin-top: 15px; font-family: 'Bodoni Moda', serif; font-style: italic; color: #94A3B8; text-align: left; }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 4. GŁÓWNA LOGIKA RYTUAŁU
# =========================================================

# Inicjalizacja stanu
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.finished = False
    st.session_state.scenario = None

# APLIKOWANIE STYLI
apply_styles()

st.markdown('<div class="brand-title">SZEPT</div><div class="brand-sub">architektura wspólnego echa</div>', unsafe_allow_html=True)

# START: Generowanie unikalnego pytania jeśli brak
if "qs" not in st.session_state:
    with st.spinner("Budowanie przestrzeni..."):
        q = call_gemini("Zadaj jedno bardzo poetyckie, ulotne pytanie otwierające. Unikaj banałów.", "Jesteś mistrzem nastroju.")
        st.session_state.qs = [q if q else "Co dziś w Tobie milczy?"]

# --- PRZEBIEG RYTUAŁU ---
if not st.session_state.finished:
    current_q = st.session_state.qs[st.session_state.step]
    
    st.markdown(f'<div class="card"><div style="font-size:1.4rem; font-weight:100;">{current_q}</div></div>', unsafe_allow_html=True)

    with st.form("ritual_form", clear_on_submit=True):
        ans = st.text_area("", height=150, placeholder="Twoje słowa...")
        _, c2, _ = st.columns([1,1,1])
        if c2.form_submit_button("UWOLNIJ SZEPT"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    with st.spinner("Wsłuchiwanie się..."):
                        sc = call_gemini(f"Wybierz: spokój, ciekawość, zmęczenie, kontakt, introspekcja, lekkość, chaos. Odp: {ans}")
                        st.session_state.scenario = sc.strip().lower() if sc else "introspekcja"
                        # Generowanie pytań 2 i 3 na podstawie odpowiedzi 1
                        q_raw = call_gemini(f"Zadaj dwa pytania dla osoby, która czuje {st.session_state.scenario}. Rozdziel średnikiem.")
                        if q_raw: st.session_state.qs.extend([x.strip() for x in q_raw.split(";")][:2])
                        else: st.session_state.qs.extend(["Co czujesz?", "Dokąd to prowadzi?"])
                
                if st.session_state.step < 2:
                    st.session_state.step += 1
                else:
                    st.session_state.finished = True
                st.rerun()

# --- WIDOK KOŃCOWY (AURA I SALA ECHO) ---
else:
    if "aura_data" not in st.session_state:
        with st.spinner("Szukanie Twojej częstotliwości..."):
            sys = """Zwróć WYŁĄCZNIE JSON: 
            {"aura": "nazwa", "tone": "opis wizualny", "hex": "#kolor", "insight": "głęboka analiza", "quote": "sentencja"}"""
            res = call_gemini(f"Analiza rytuału: {st.session_state.answers}", sys, is_json=True)
            try:
                st.session_state.aura_data = json.loads(res)
                # Zapis do bazy
                if db:
                    db.collection('artifacts').document(APP_ID).collection('public').document('data').collection('whispers').add({
                        "text": st.session_state.answers[-1], 
                        "aura": st.session_state.aura_data['aura'], 
                        "scenario": st.session_state.scenario, 
                        "timestamp": firestore.SERVER_TIMESTAMP
                    })
            except:
                st.session_state.aura_data = {"aura": "Głębokie Echo", "tone": "Czerń", "hex": "#10131A", "insight": "Cisza.", "quote": "..."}

    aura = st.session_state.aura_data
    apply_styles(aura['hex']) # Dynamiczne tło aury

    st.markdown(f"""
    <div class="card">
        <div style="font-size:0.7rem; letter-spacing:0.5rem; color:#475569; margin-bottom:20px;">PROFIL OBECNOŚCI</div>
        <div style="font-size:3.5rem; font-family:'Bodoni Moda', serif;">{aura['aura']}</div>
        <div style="color:{aura['hex']}; font-size:0.8rem; letter-spacing:0.2rem; margin:10px 0;">{aura['tone'].upper()}</div>
        <hr style="border-color:rgba(255,255,255,0.05); margin:30px 0;">
        <div style="color:#CBD5E1; line-height:1.8; font-weight:200;">{aura['insight']}</div>
        <div style="font-style:italic; color:#64748B; margin-top:30px;">"{aura['quote']}"</div>
    </div>
    """, unsafe_allow_html=True)

    # SALA ECHO
    st.markdown('<div style="text-align:center; margin-top:60px; color:#1E293B; letter-spacing:0.4rem; font-size:0.75rem;">SALA ECHO</div>', unsafe_allow_html=True)
    if db:
        docs = db.collection('artifacts').document(APP_ID).collection('public').document('data').collection('whispers').limit(20).stream()
        matches = [d.to_dict() for d in docs if d.to_dict().get('scenario') == st.session_state.scenario]
        if matches:
            for e in random.sample(matches, min(len(matches), 3)):
                st.markdown(f'<div class="echo-card"><div style="font-size:0.6rem; color:#334155; margin-bottom:5px;">{e["aura"].upper()}</div>"{e["text"]}"</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center; color:#334155; margin-top:20px;">Cisza. Jesteś pierwszym echem.</div>', unsafe_allow_html=True)

    if st.button("ROZPOCZNIJ OD NOWA"):
        st.session_state.clear()
        st.rerun()
