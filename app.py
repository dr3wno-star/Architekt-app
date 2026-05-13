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

.progress {
    text-align: center;
    color: #334155;
    margin-bottom: 15px;
    letter-spacing: 0.2rem;
    font-size: 0.7rem;
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
    animation: slowAppear 2s ease;
}

.aura-desc {
    margin-top: 30px;
    color: #94A3B8;
    line-height: 2rem;
    font-size: 1.05rem;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
    animation: slowAppear 3s ease;
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
    animation: slowAppear 3.5s ease;
}

.level {
    margin-top: 45px;
    color: #475569;
    letter-spacing: 0.2rem;
    font-size: 0.75rem;
    line-height: 1.9;
    animation: slowAppear 4s ease;
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
# PYTANIA
# =========================================================

QUESTION_BANK = [

    "Za czym tęskni Twoja głowa, kiedy robi się całkiem cicho?",

    "Czego najbardziej boisz się w kontakcie z nową osobą?",

    "Jak wygląda miejsce, w którym naprawdę odpoczywasz?",

    "Która emocja wraca do Ciebie najczęściej nocą?",

    "Co ukrywasz pod spokojem?",

    "Jakiej obecności najbardziej brakuje Ci w życiu?",

    "Co chciałbyś usłyszeć od drugiego człowieka?",

    "Kiedy ostatni raz poczułeś prawdziwe zrozumienie?",

    "Jakiej ciszy potrzebujesz najbardziej?",

    "Co męczy Cię w relacjach z ludźmi?",

    "Jak wygląda Twoje emocjonalne schronienie?",

    "Jaką część siebie pokazujesz najrzadziej?"
]

# =========================================================
# FALLBACK AUR
# =========================================================

FALLBACK_AURAS = [

    {
        "aura": "Cichy Ogień",
        "description": "Ukrywasz intensywność pod spokojną powierzchnią.",
        "traits": [
            "introspekcja",
            "ostrożność",
            "głębia"
        ],
        "next_path": "nocna rozmowa",
        "whisper_level": 2
    },

    {
        "aura": "Nocne Echo",
        "description": "Twoje emocje długo rezonują w ciszy.",
        "traits": [
            "melancholia",
            "uważność",
            "delikatność"
        ],
        "next_path": "archiwum ciszy",
        "whisper_level": 3
    },

    {
        "aura": "Miękki Mrok",
        "description": "Chronisz swoją wrażliwość przed hałasem świata.",
        "traits": [
            "spokój",
            "samotność",
            "obserwacja"
        ],
        "next_path": "głębokie echo",
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

if "questions" not in st.session_state:
    st.session_state.questions = random.sample(QUESTION_BANK, 3)

if "current_answer" not in st.session_state:
    st.session_state.current_answer = ""

# =========================================================
# AI ANALIZA
# =========================================================

def analyze_with_ai(answers):

    if not model:
        return random.choice(FALLBACK_AURAS)

    prompt = f"""
    Jesteś poetą-psychologiem ambientowej aplikacji SZEPT.

    Analizujesz emocjonalny klimat wypowiedzi użytkownika.

    Odpowiedzi użytkownika:
    {answers}

    Zwróć WYŁĄCZNIE poprawny JSON.

    FORMAT:

    {{
      "aura": "krótka poetycka nazwa",
      "description": "jedno subtelne poetyckie zdanie",
      "traits": ["cecha1", "cecha2", "cecha3"],
      "next_path": "nazwa ścieżki",
      "whisper_level": liczba 1-5
    }}

    ZASADY:
    - melancholijnie
    - subtelnie
    - spokojnie
    - bez diagnoz
    - bez oceniania
    - krótko
    - po polsku
    """

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        if "```json" in text:
            text = text.replace("```json", "")
            text = text.replace("```", "")

        data = json.loads(text)

        return data

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

    answer = st.text_area(
        "",
        height=160,
        placeholder="Pozwól myśli wybrzmieć...",
        key="current_answer"
    )

    c1, c2, c3 = st.columns([1,1,1])

    with c2:

        if st.button("UWOLNIJ SZEPT"):

            if answer.strip():

                st.session_state.answers.append(answer)

                st.session_state.current_answer = ""

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

        aura = analyze_with_ai(st.session_state.answers)

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
