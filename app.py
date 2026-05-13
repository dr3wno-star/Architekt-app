import streamlit as st
import google.generativeai as genai
import random
import time
import json

# =========================================================
# KONFIGURACJA
# =========================================================

st.set_page_config(
    page_title="SZEPT",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GEMINI API
# =========================================================

API_KEY = "AIzaSyBfyfqZfLvfAa9vamqATwwnzvBHD25jmoc"

@st.cache_resource
def init_ai():

    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash")

    except:
        return None

model = init_ai()

# =========================================================
# STYL
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400;500&family=Inter:wght@200;300;400;500&display=swap');

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
    radial-gradient(circle at top, #10131A 0%, #08080A 45%);
    color: #E2E8F0;
}

.block-container {
    padding-top: 2rem;
    max-width: 760px;
}

.brand {
    text-align: center;
    margin-top: 70px;
    margin-bottom: 60px;
    animation: fadeIn 1.5s ease;
}

.brand-title {
    font-size: 3.2rem;
    font-weight: 200;
    letter-spacing: 1rem;
    color: #F8FAFC;
}

.brand-sub {
    margin-top: 12px;
    color: #475569;
    font-style: italic;
    font-family: 'Bodoni Moda', serif;
    letter-spacing: 0.15rem;
}

.progress {
    text-align: center;
    color: #334155;
    margin-bottom: 15px;
    letter-spacing: 0.2rem;
    font-size: 0.7rem;
}

.question-card {
    padding: 45px;
    border: 1px solid rgba(255,255,255,0.05);
    background: rgba(255,255,255,0.015);
    backdrop-filter: blur(10px);
    margin-bottom: 25px;
    animation: fadeIn 1s ease;
}

.question-text {
    font-size: 1.35rem;
    line-height: 2rem;
    text-align: center;
    color: #CBD5E1;
    font-weight: 300;
}

textarea {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #1E293B !important;
    color: white !important;
    text-align: center !important;
    font-size: 1.05rem !important;
}

textarea:focus {
    box-shadow: none !important;
}

.stButton button {
    width: 100%;
    background: transparent !important;
    border: 1px solid #1E293B !important;
    color: #94A3B8 !important;
    padding: 0.85rem 2rem !important;
    border-radius: 0px !important;
    transition: 0.4s;
    letter-spacing: 0.15rem;
}

.stButton button:hover {
    border-color: #334155 !important;
    color: white !important;
}

.aura-box {
    padding: 65px 45px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.06);
    background: rgba(255,255,255,0.02);
    backdrop-filter: blur(15px);
    animation: slowAppear 2s ease;
}

.aura-title {
    color: #64748B;
    font-size: 0.75rem;
    letter-spacing: 0.35rem;
    text-transform: uppercase;
}

.aura-name {
    font-size: 3.4rem;
    margin-top: 25px;
    color: #F8FAFC;
    font-family: 'Bodoni Moda', serif;
    line-height: 1.2;
    letter-spacing: 0.08rem;
}

.aura-desc {
    margin-top: 30px;
    color: #94A3B8;
    line-height: 2rem;
    font-size: 1.05rem;
    max-width: 520px;
    margin-left: auto;
    margin-right: auto;
}

.traits {
    margin-top: 40px;
}

.trait {
    display: inline-block;
    padding: 8px 14px;
    margin: 5px;
    border: 1px solid #1E293B;
    color: #94A3B8;
    font-size: 0.85rem;
    letter-spacing: 0.05rem;
}

.level {
    margin-top: 45px;
    color: #475569;
    letter-spacing: 0.2rem;
    font-size: 0.75rem;
    line-height: 1.9;
}

.divider {
    margin-top: 50px;
    margin-bottom: 40px;
    border-color: #111827;
}

@keyframes fadeIn {

    from {
        opacity:0;
        transform: translateY(12px);
    }

    to {
        opacity:1;
        transform: translateY(0px);
    }
}

@keyframes slowAppear {

    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PIERWSZE PYTANIA KOMPASOWE
# =========================================================

FIRST_QUESTIONS = [

    "Z czym przychodzisz dziś do tej przestrzeni?",

    "Co dziś najbardziej zajmowało Twoją głowę?",

    "Jak wyglądał Twój dzień od środka?",

    "Jakiej energii najbardziej Ci dziś brakuje?",

    "Co dziś najmocniej zostało z Tobą po całym dniu?"
]

# =========================================================
# SCENARIUSZE
# =========================================================

SCENARIOS = {

    "spokój": [

        "Co pomaga Ci naprawdę zwolnić?",

        "W jakim miejscu czujesz największy wewnętrzny oddech?"
    ],

    "ciekawość": [

        "Jakiej rozmowy chciałbyś dziś doświadczyć?",

        "Co ostatnio najbardziej Cię zaintrygowało?"
    ],

    "zmęczenie": [

        "Co najbardziej odbiera Ci energię?",

        "Jak wyglądałby Twój idealny moment wyciszenia?"
    ],

    "kontakt": [

        "Jakiej obecności najbardziej Ci dziś brakuje?",

        "Co sprawia, że czujesz prawdziwe połączenie z drugim człowiekiem?"
    ],

    "introspekcja": [

        "Jaką część siebie pokazujesz najrzadziej?",

        "Która myśl wraca do Ciebie najczęściej w ciszy?"
    ],

    "lekkość": [

        "Co ostatnio wywołało u Ciebie autentyczny uśmiech?",

        "Jak wygląda moment, w którym czujesz pełną swobodę?"
    ],

    "chaos": [

        "Co dziś było w Tobie najbardziej niespokojne?",

        "Za czym najbardziej tęskni Twoja głowa, gdy wszystko cichnie?"
    ]
}

# =========================================================
# FALLBACK AURY
# =========================================================

FALLBACK_AURAS = [

    {
        "aura": "Spokojne Echo",
        "description": "Wnosisz do przestrzeni miękką uważność.",
        "traits": ["spokój", "obserwacja", "autentyczność"],
        "next_path": "cicha rozmowa",
        "whisper_level": 2
    },

    {
        "aura": "Świetliste Tło",
        "description": "Twoja energia pozostawia po sobie delikatny ślad.",
        "traits": ["lekkość", "obecność", "ciekawość"],
        "next_path": "nocne echo",
        "whisper_level": 3
    },

    {
        "aura": "Głębokie Echo",
        "description": "Myślisz głębiej niż pokazujesz światu.",
        "traits": ["introspekcja", "emocjonalność", "uważność"],
        "next_path": "rytuał ciszy",
        "whisper_level": 4
    }

]

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

    first_question = random.choice(FIRST_QUESTIONS)

    st.session_state.questions = [first_question]

# =========================================================
# AI WYBÓR SCENARIUSZA
# =========================================================

def detect_scenario(first_answer):

    if not model:
        return random.choice(list(SCENARIOS.keys()))

    prompt = f"""
    Użytkownik odpowiedział:

    "{first_answer}"

    Wybierz jeden najlepiej pasujący kierunek emocjonalny.

    Dostępne kierunki:

    - spokój
    - ciekawość
    - zmęczenie
    - kontakt
    - introspekcja
    - lekkość
    - chaos

    Zwróć WYŁĄCZNIE nazwę kierunku.
    """

    try:

        response = model.generate_content(prompt)

        scenario = response.text.strip().lower()

        if scenario in SCENARIOS:
            return scenario

        return random.choice(list(SCENARIOS.keys()))

    except:
        return random.choice(list(SCENARIOS.keys()))

# =========================================================
# AI AURA
# =========================================================

def analyze_with_ai(answers, scenario):

    if not model:
        return random.choice(FALLBACK_AURAS)

    prompt = f"""
    Jesteś poetą-psychologiem aplikacji SZEPT.

    Kierunek emocjonalny:
    {scenario}

    Odpowiedzi użytkownika:
    {answers}

    Zwróć WYŁĄCZNIE poprawny JSON.

    FORMAT:

    {{
      "aura": "krótka poetycka nazwa",
      "description": "jedno subtelne zdanie",
      "traits": ["cecha1", "cecha2", "cecha3"],
      "next_path": "nazwa ścieżki",
      "whisper_level": liczba 1-5
    }}

    ZASADY:
    - subtelnie
    - emocjonalnie
    - bez diagnoz
    - bez mroku na siłę
    - naturalnie
    - po polsku
    """

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        if "```json" in text:
            text = text.replace("```json", "")
            text = text.replace("```", "")

        return json.loads(text)

    except:
        return random.choice(FALLBACK_AURAS)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="brand">
    <div class="brand-title">SZEPT</div>
    <div class="brand-sub">Where conversations breathe</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FLOW
# =========================================================

if not st.session_state.finished:

    current_question = st.session_state.questions[st.session_state.step]

    st.markdown(f"""
    <div class="progress">
        RYTUAŁ {st.session_state.step + 1} / 3
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="question-card">
        <div class="question-text">
            {current_question}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("whisper_form", clear_on_submit=True):

        answer = st.text_area(
            "",
            height=160,
            placeholder="Pozwól myśli wybrzmieć..."
        )

        c1, c2, c3 = st.columns([1,1,1])

        with c2:

            submitted = st.form_submit_button("UWOLNIJ SZEPT")

        if submitted:

            if answer.strip():

                st.session_state.answers.append(answer)

                # =====================================================
                # PO PIERWSZEJ ODPOWIEDZI
                # =====================================================

                if st.session_state.step == 0:

                    detected = detect_scenario(answer)

                    st.session_state.scenario = detected

                    next_questions = SCENARIOS[detected]

                    st.session_state.questions.extend(next_questions)

                # =====================================================
                # PRZEJŚCIA
                # =====================================================

                if st.session_state.step < 2:
                    st.session_state.step += 1

                else:
                    st.session_state.finished = True

                st.rerun()

# =========================================================
# WYNIK
# =========================================================

else:

    with st.spinner("Architekt wsłuchuje się w Twoje echo..."):

        time.sleep(2)

        aura = analyze_with_ai(
            st.session_state.answers,
            st.session_state.scenario
        )

    st.markdown("""
    <div class="aura-box">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="aura-title">
        TWOJA AURA
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="aura-name">
        {aura["aura"]}
    </div>

    <div class="aura-desc">
        {aura["description"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="traits">
    """, unsafe_allow_html=True)

    for trait in aura["traits"]:

        st.markdown(
            f"<span class='trait'>{trait}</span>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="level">

        WHISPER LEVEL • {aura["whisper_level"]}

        <br><br>

        ODBLOKOWANA ŚCIEŻKA • {aura["next_path"].upper()}

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr class="divider">
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:

        if st.button("POWRÓĆ DO RYTUAŁU"):

            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()
