import streamlit as st
import google.generativeai as genai
import random
import time
import json

# =========================================================
# KONFIGURACJA STRONY
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# BEZPIECZEŃSTWO API
# =========================================================
# Aby to działało, dodaj klucz w pliku .streamlit/secrets.toml:
# GEMINI_KEY = "TWOJ_KLUCZ_API"

API_KEY = st.secrets.get("GEMINI_KEY", "")

@st.cache_resource
def init_ai():
    if not API_KEY:
        return None
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None

model = init_ai()

# =========================================================
# SESSION STATE
# =========================================================

if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "finished" not in st.session_state:
    st.session_state.finished = False
if "scenario" not in st.session_state:
    st.session_state.scenario = None
if "questions" not in st.session_state:
    FIRST_QUESTIONS = [
        "Z czym przychodzisz dziś do tej przestrzeni?",
        "Co dziś najbardziej zajmowało Twoją głowę?",
        "Jak wyglądał Twój dzień od środka?",
        "Jakiej energii najbardziej Ci dziś brakuje?",
        "Co dziś najmocniej zostało z Tobą po całym dniu?"
    ]
    st.session_state.questions = [random.choice(FIRST_QUESTIONS)]

# =========================================================
# DYNAMICZNY STYL (CSS)
# =========================================================

# Kolory zależne od nastroju/scenariusza
MOOD_COLORS = {
    "spokój": "#0B1014",      # Głęboki granat/czerń
    "ciekawość": "#0D1321",   # Nocne niebo
    "zmęczenie": "#09090B",   # Absolutna czerń
    "kontakt": "#16161D",     # Ciepły grafit
    "introspekcja": "#101014",# Czysta czerń
    "lekkość": "#141B24",     # Stalowy błękit
    "chaos": "#1A1414",       # Czerń z domieszką burgundu
    None: "#10131A"           # Domyślny
}

current_mood_bg = MOOD_COLORS.get(st.session_state.scenario, "#10131A")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,500;1,400&family=Inter:wght@200;300;400;500&display=swap');

/* Reset i Główne Tło */
#MainMenu, footer, header {{visibility:hidden;}}

.stApp {{
    background: radial-gradient(circle at top, {current_mood_bg} 0%, #08080A 45%) !important;
    color: #E2E8F0;
    transition: background 3s ease-in-out;
}}

.block-container {{
    padding-top: 2rem;
    max-width: 760px;
}}

/* Branding */
.brand {{
    text-align: center;
    margin-top: 50px;
    margin-bottom: 40px;
    animation: fadeIn 2s ease;
}}

.brand-title {{
    font-size: 3.5rem;
    font-weight: 200;
    letter-spacing: 1.2rem;
    color: #F8FAFC;
    margin-bottom: 0;
}}

.brand-sub {{
    margin-top: 8px;
    color: #475569;
    font-style: italic;
    font-family: 'Bodoni Moda', serif;
    letter-spacing: 0.2rem;
    font-size: 0.9rem;
}}

/* Pytania i Formularz */
.question-card {{
    padding: 60px 40px;
    border: 1px solid rgba(255,255,255,0.03);
    background: rgba(255,255,255,0.01);
    backdrop-filter: blur(20px);
    margin-bottom: 30px;
    border-radius: 2px;
    text-align: center;
}}

.question-text {{
    font-size: 1.45rem;
    line-height: 2.2rem;
    color: #CBD5E1;
    font-weight: 300;
    animation: typewriter 2s steps(40);
    overflow: hidden;
    white-space: normal;
}}

textarea {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #1E293B !important;
    color: #F8FAFC !important;
    text-align: center !important;
    font-size: 1.1rem !important;
    padding: 20px !important;
    transition: 0.6s !important;
}}

textarea:focus {{
    border-bottom: 1px solid #475569 !important;
    box-shadow: none !important;
    background: rgba(255,255,255,0.02) !important;
}}

.stButton button {{
    width: 100%;
    background: transparent !important;
    border: 1px solid #1E293B !important;
    color: #64748B !important;
    padding: 0.9rem !important;
    border-radius: 0px !important;
    letter-spacing: 0.3rem;
    transition: 0.5s;
    text-transform: uppercase;
    font-size: 0.75rem;
}}

.stButton button:hover {{
    border-color: #94A3B8 !important;
    color: white !important;
    background: rgba(255,255,255,0.03) !important;
}}

/* Aura / Wynik */
.aura-box {{
    padding: 80px 45px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    background: rgba(255,255,255,0.015);
    animation: slowAppear 3s ease;
}}

.aura-name {{
    font-size: 3.8rem;
    color: #F8FAFC;
    font-family: 'Bodoni Moda', serif;
    margin: 25px 0;
    letter-spacing: 0.1rem;
}}

.whisper-quote {{
    margin: 35px auto;
    font-style: italic;
    color: #64748B;
    font-family: 'Bodoni Moda', serif;
    font-size: 1.25rem;
    max-width: 80%;
    line-height: 1.8;
}}

.trait {{
    display: inline-block;
    padding: 6px 16px;
    margin: 6px;
    border: 1px solid rgba(255,255,255,0.08);
    color: #94A3B8;
    font-size: 0.8rem;
    letter-spacing: 0.1rem;
    text-transform: lowercase;
}}

/* Animacje */
@keyframes typewriter {{
    from {{ opacity: 0; transform: translateY(5px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

@keyframes slowAppear {{
    from {{ opacity: 0; transform: scale(0.98); }}
    to {{ opacity: 1; transform: scale(1); }}
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIKA AI
# =========================================================

def detect_scenario(first_answer):
    SCENARIOS_LIST = ["spokój", "ciekawość", "zmęczenie", "kontakt", "introspekcja", "lekkość", "chaos"]
    if not model: return random.choice(SCENARIOS_LIST)
    
    prompt = f"Analizuj odpowiedź: '{first_answer}'. Wybierz jeden kierunek z: {', '.join(SCENARIOS_LIST)}. Zwróć tylko jedno słowo."
    try:
        response = model.generate_content(prompt)
        res = response.text.strip().lower()
        return res if res in SCENARIOS_LIST else "introspekcja"
    except:
        return "introspekcja"

def analyze_with_ai(answers, scenario):
    if not model:
        return {
            "aura": "Ciche Echo",
            "description": "Twoja obecność jest jak mgła nad taflą jeziora.",
            "traits": ["cisza", "uważność"],
            "next_path": "ścieżka cienia",
            "whisper_level": 3,
            "whisper_quote": "W milczeniu ukryta jest największa siła."
        }

    prompt = f"""
    Jesteś poetą-psychologiem aplikacji SZEPT. 
    Analizuj te głosy: {answers} (Kierunek: {scenario}).
    Zwróć JSON:
    {{
      "aura": "krótka poetycka nazwa (np. Księżycowy Pył)",
      "description": "subtelne zdanie opisu",
      "traits": ["cecha1", "cecha2", "cecha3"],
      "next_path": "nazwa kolejnego etapu",
      "whisper_level": 1-5,
      "whisper_quote": "jedna unikalna, mistyczna sentencja napisana dla tego użytkownika"
    }}
    Styl: Polski, elegancki, minimalistyczny.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        return json.loads(text)
    except:
        return {"aura": "Nienazwane", "description": "Echo, które nie znalazło jeszcze formy.", "traits": ["niepewność"], "next_path": "powrót", "whisper_level": 1, "whisper_quote": "Pytania są ważniejsze niż odpowiedzi."}

# =========================================================
# INTERFEJS RYTUAŁU
# =========================================================

st.markdown("""
<div class="brand">
    <div class="brand-title">SZEPT</div>
    <div class="brand-sub">konwersacja, która oddycha</div>
</div>
""", unsafe_allow_html=True)

SCENARIO_DATA = {
    "spokój": ["Co pomaga Ci naprawdę zwolnić?", "W jakim miejscu czujesz największy wewnętrzny oddech?"],
    "ciekawość": ["Jakiej rozmowy chciałbyś dziś doświadczyć?", "Co ostatnio najbardziej Cię zaintrygowało?"],
    "zmęczenie": ["Co najbardziej odbiera Ci energię?", "Jak wyglądałby Twój idealny moment wyciszenia?"],
    "kontakt": ["Jakiej obecności najbardziej Ci dziś brakuje?", "Co sprawia, że czujesz prawdziwe połączenie?"],
    "introspekcja": ["Jaką część siebie pokazujesz najrzadziej?", "Która myśl wraca do Ciebie najczęściej w ciszy?"],
    "lekkość": ["Co ostatnio wywołało u Ciebie uśmiech?", "Jak wygląda moment pełnej swobody?"],
    "chaos": ["Co dziś było w Tobie najbardziej niespokojne?", "Za czym tęskni Twoja głowa, gdy wszystko cichnie?"]
}

if not st.session_state.finished:
    current_q = st.session_state.questions[st.session_state.step]
    
    st.markdown(f"""
    <div style="text-align:center; color:#334155; font-size:0.7rem; letter-spacing:0.3rem; margin-bottom:15px;">
        ETAP {st.session_state.step + 1} / 3
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="question-card">
        <div class="question-text">{current_q}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("whisper_form", clear_on_submit=True):
        answer = st.text_area("", height=180, placeholder="Pozwól myślom płynąć...")
        _, c2, _ = st.columns([1, 1.2, 1])
        with c2:
            submitted = st.form_submit_button("UWOLNIJ SZEPT")
        
        if submitted and answer.strip():
            st.session_state.answers.append(answer)
            
            if st.session_state.step == 0:
                with st.spinner("Wsłuchiwanie się w ton..."):
                    scenario = detect_scenario(answer)
                    st.session_state.scenario = scenario
                    st.session_state.questions.extend(SCENARIO_DATA.get(scenario, SCENARIO_DATA["introspekcja"]))
            
            if st.session_state.step < 2:
                st.session_state.step += 1
            else:
                st.session_state.finished = True
            st.rerun()

# =========================================================
# WYNIK (AURA)
# =========================================================

else:
    with st.spinner("Architekt splata Twoje echa..."):
        time.sleep(2.5)
        aura = analyze_with_ai(st.session_state.answers, st.session_state.scenario)

    st.markdown(f"""
    <div class="aura-box">
        <div style="color: #64748B; font-size: 0.7rem; letter-spacing: 0.4rem; text-transform: uppercase;">Twoja Aura</div>
        <div class="aura-name">{aura.get('aura', '---')}</div>
        <div class="aura-desc">{aura.get('description', '')}</div>
        <div class="whisper-quote">"{aura.get('whisper_quote', '')}"</div>
        <div style="margin-top: 30px;">
            {' '.join([f'<span class="trait">{t}</span>' for t in aura.get('traits', [])])}
        </div>
        <div style="margin-top: 50px; color: #334155; font-size: 0.75rem; letter-spacing: 0.2rem;">
            WHISPER LEVEL • {aura.get('whisper_level', 1)}<br><br>
            ŚCIEŻKA • {aura.get('next_path', '').upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.button("ROZPOCZNIJ OD NOWA"):
            st.session_state.clear()
            st.rerun()
