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
    except: return None

db = init_db()
GEMINI_KEY = st.secrets.get("GEMINI_KEY")

# =========================================================
# 2. SILNIK NIEPRZEWIDYWALNOŚCI
# =========================================================

def call_ai(prompt, system_prompt="", is_json=False):
    if not GEMINI_KEY: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 1.0, 
            "responseMimeType": "application/json" if is_json else "text/plain"
        }
    }
    try:
        r = requests.post(url, json=payload, timeout=25)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except: return None

# Role, które AI przyjmuje, by zadawać pytania - to gwarantuje różnorodność
ROLES = [
    "Surowy analityk danych, który szuka błędu w ludzkich emocjach.",
    "Stary introligator, który patrzy na ludzi jak na zużyte książki.",
    "Architekt, który widzi w emocjach jedynie konstrukcje i naprężenia.",
    "Ktoś, kto nie spał od trzech dób i widzi świat zbyt wyraźnie.",
    "Rzeźbiarz, który szuka w Twoich słowach zbędnego materiału do odcięcia."
]

# =========================================================
# 3. LOGIKA I STYLE
# =========================================================

if "qs" not in st.session_state:
    role = random.choice(ROLES)
    with st.spinner("Architekt zmienia postać..."):
        q = call_ai(
            "Zadaj jedno, niezwykle specyficzne i nieoczekiwane pytanie otwierające. Niech dotyczy detalu, o którym rzadko się myśli. Unikaj poezji, szukaj konkretu.",
            f"Twoja rola: {role}. Nienawidzisz ogólników."
        )
        st.session_state.qs = [q if q else "Gdzie w Twoim ciele mieszka dzisiaj Twój najgorszy nawyk?"]
        st.session_state.step, st.session_state.answers, st.session_state.finished, st.session_state.scenario = 0, [], False, None

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;300;400&display=swap');
#MainMenu, footer, header {{visibility:hidden;}}
.stApp {{ background: #08080A !important; color: #E2E8F0; }}
.card {{ padding: 60px 40px; border: 1px solid rgba(255,255,255,0.03); background: rgba(255,255,255,0.005); text-align: center; }}
textarea {{ background: transparent !important; border: none !important; border-bottom: 1px solid #1E293B !important; color: #F8FAFC !important; text-align: center !important; font-size: 1.2rem !important; }}
.stButton button {{ width: 100%; background: transparent !important; border: 1px solid #1E293B !important; color: #475569 !important; letter-spacing: 0.3rem; padding: 1rem !important; }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 4. PRZEBIEG RYTUAŁU
# =========================================================

st.markdown('<h1 style="text-align:center; font-weight:100; letter-spacing:1.2rem; margin-top:50px;">SZEPT</h1>', unsafe_allow_html=True)

if not st.session_state.finished:
    cur_q = st.session_state.qs[st.session_state.step]
    st.markdown(f'<div class="card"><div style="font-size:1.4rem; font-weight:100;">{cur_q}</div></div>', unsafe_allow_html=True)

    with st.form("main_form", clear_on_submit=True):
        ans = st.text_area("", height=150, placeholder="Twoje słowa...")
        if st.form_submit_button("UWOLNIJ"):
            if ans.strip():
                st.session_state.answers.append(ans)
                if st.session_state.step == 0:
                    with st.spinner("Przesiewanie..."):
                        # Kolejne pytania generowane są dynamicznie na podstawie odpowiedzi
                        q_next = call_ai(
                            f"Użytkownik odpowiedział: '{ans}'. Zadaj dwa kolejne pytania, które nie dają spokoju i wymagają konkretnej odpowiedzi. Rozdziel średnikiem.",
                            "Jesteś dociekliwy do bólu. Nie akceptujesz metafor."
                        )
                        st.session_state.qs.extend([x.strip() for x in q_raw.split(";")][:2] if q_next else ["Co to zmienia?", "Dlaczego teraz?"])
                
                if st.session_state.step < 2: st.session_state.step += 1
                else: st.session_state.finished = True
                st.rerun()

else:
    # ANALIZA FINALNA - ZAMIAST OGÓLNIKÓW, SZUKAMY KRAWĘDZI
    if "aura" not in st.session_state:
        with st.spinner("Kończenie zapisu..."):
            sys = """Zwróć WYŁĄCZNIE JSON: 
            {"name": "nazwa stanu jako zjawisko fizyczne", "hex": "#kolor", "insight": "analiza Twojej konkretnej sytuacji, bez lania wody", "recommendation": "jedna, nietypowa czynność do wykonania teraz"}"""
            res = call_ai(f"Analizuj bez ogródek te odpowiedzi: {st.session_state.answers}", sys, is_json=True)
            try: st.session_state.aura = json.loads(res)
            except: st.session_state.aura = {"name": "Stan Statyczny", "hex": "#1E293B", "insight": "Twoje echo jest zbyt ciche dla algorytmu.", "recommendation": "Wyłącz ekrany na 10 minut."}

    a = st.session_state.aura
    st.markdown(f"""
    <div class="card" style="border-color:{a['hex']}">
        <div style="font-size:0.6rem; letter-spacing:0.5rem; color:#475569; margin-bottom:15px;">ECHO KOŃCOWE</div>
        <div style="font-size:3rem; font-family:serif; color:{a['hex']}">{a['name']}</div>
        <div style="margin:30px 0; color:#CBD5E1; line-height:1.6; font-weight:300;">{a['insight']}</div>
        <div style="font-size:0.8rem; color:{a['hex']}; letter-spacing:0.1rem; border: 1px solid {a['hex']}; padding: 10px; display: inline-block;">
            ZADANIE: {a['recommendation'].upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("RESET"):
        st.session_state.clear()
        st.rerun()
