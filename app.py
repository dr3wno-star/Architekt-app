import streamlit as st
import time
import html
from dataclasses import dataclass, asdict
from typing import List

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="The Architect | Resonance Gateway",
    page_icon="🏛️",
    layout="centered"
)

# =========================================================
# STYLES
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, #17202B 0%, transparent 35%),
        radial-gradient(circle at bottom right, #10151C 0%, transparent 35%),
        #0B0F14;
    color: #E6EDF3;
}

/* HEADER */

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 5px;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    color: #8B9BAB;
    margin-bottom: 35px;
    font-size: 1rem;
}

/* ARCHITECT MESSAGE */

.architect-box {
    background: linear-gradient(145deg, #161B22, #11161D);
    border: 1px solid #2D3742;
    border-left: 5px solid #4A90E2;
    padding: 24px;
    border-radius: 18px;
    margin-top: 20px;
    margin-bottom: 20px;
    line-height: 1.8;
    color: #D6E2EE;
    animation: fadeIn 0.4s ease-in-out;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* USER MESSAGE */

.user-box {
    background: #0F141B;
    border: 1px solid #29313A;
    padding: 18px;
    border-radius: 16px;
    margin-top: 15px;
    margin-bottom: 10px;
    color: #C9D1D9;
}

/* ANALYSIS */

.analysis-box {
    background: #131920;
    border: 1px solid #26303A;
    border-radius: 14px;
    padding: 18px;
    color: #AEBCCA;
    line-height: 1.8;
}

/* TAGS */

.tag {
    display: inline-block;
    background: #1E2935;
    color: #8FC7FF;
    padding: 5px 10px;
    margin: 4px;
    border-radius: 999px;
    font-size: 0.8rem;
}

/* SCORE */

.score-good {
    color: #6EE7B7;
    font-weight: 600;
}

.score-neutral {
    color: #FACC15;
    font-weight: 600;
}

.score-bad {
    color: #F87171;
    font-weight: 600;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    background: linear-gradient(135deg, #3081D0, #1E5EA8);
    color: white;
    border: none;
    padding: 0.8rem;
    font-size: 1rem;
    font-weight: 500;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(48,129,208,0.35);
}

/* TEXT AREA */

textarea {
    border-radius: 14px !important;
    background-color: #11161D !important;
    color: #E6EDF3 !important;
    border: 1px solid #2C3742 !important;
}

/* PROGRESS */

.progress-label {
    text-align: center;
    margin-top: 15px;
    color: #8B9BAB;
}

/* FINAL MESSAGE */

.final-box {
    background: linear-gradient(145deg, #131A22, #10151C);
    border: 1px solid #26303A;
    border-left: 5px solid #6EE7B7;
    padding: 24px;
    border-radius: 18px;
    margin-top: 25px;
    line-height: 1.8;
    color: #DDE7F1;
}

/* ANIMATION */

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SCENARIO
# =========================================================

SCENARIO = [
    "Witaj w przestrzeni, gdzie rozmowa ma znaczenie. Co sprawiło, że właśnie dziś poczułeś potrzebę bycia wysłuchanym?",

    "Wiele osób nosi w sobie rzeczy, których nigdy nie wypowiada na głos. O czym najtrudniej Ci mówić innym ludziom?",

    "Każdy człowiek szuka czegoś innego: spokoju, zrozumienia, bliskości lub ciszy. Czego najbardziej brakuje Tobie?",

    "Dziękuję za Twoją szczerość. System analizuje styl komunikacji, aby dopasować Cię do osób o podobnym poziomie refleksyjności i emocjonalnej wrażliwości."
]

# =========================================================
# DATA MODEL
# =========================================================

@dataclass
class IntentProfile:
    empathy: int
    openness: int
    authenticity: int
    aggression: int
    humor_masking: int
    emotional_depth: int
    tags: List[str]
    warnings: List[str]
    final_score: int
    resonance: str

# =========================================================
# ANALYSIS ENGINE
# =========================================================

def analyze_intent(text: str, response_time: float) -> IntentProfile:

    text_low = text.lower()
    words = text.split()

    empathy = 0
    openness = 0
    authenticity = 0
    aggression = 0
    humor_masking = 0
    emotional_depth = 0

    tags = []
    warnings = []

    # =====================================================
    # EMOTIONAL SIGNALS
    # =====================================================

    emotional_phrases = [
        "mam wrażenie",
        "czuję",
        "czuję się",
        "boję się",
        "trudno mi",
        "brakuje mi",
        "czasami",
        "od dawna",
        "nie wiem",
        "chciałbym",
        "samotny",
        "zmęczony",
        "zagubiony",
        "tęsknię",
        "martwię się",
        "przytłacza mnie",
        "nie potrafię",
        "potrzebuję",
        "chciałbym być",
        "nie radzę sobie"
    ]

    emotional_hits = sum(
        1 for phrase in emotional_phrases
        if phrase in text_low
    )

    empathy += emotional_hits * 18

    # =====================================================
    # DEPTH DETECTION
    # =====================================================

    if len(words) > 20:
        emotional_depth += 20

    if len(words) > 40:
        emotional_depth += 20
        openness += 15

    if len(words) > 70:
        emotional_depth += 25
        openness += 20

    # =====================================================
    # PERSONAL LANGUAGE
    # =====================================================

    personal_language = [
        "ja",
        "mnie",
        "dla mnie",
        "u mnie",
        "moje",
        "myślę",
        "czuję"
    ]

    personal_hits = sum(
        1 for phrase in personal_language
        if phrase in text_low
    )

    authenticity += personal_hits * 10

    # =====================================================
    # REFLECTION DETECTION
    # =====================================================

    reflective_patterns = [
        "zastanawiam",
        "analizuję",
        "próbuję zrozumieć",
        "mam wrażenie",
        "wydaje mi się",
        "czasem myślę",
        "od pewnego czasu",
        "zauważyłem",
        "zauważyłam"
    ]

    reflection_hits = sum(
        1 for phrase in reflective_patterns
        if phrase in text_low
    )

    openness += reflection_hits * 15

    # =====================================================
    # NATURAL LANGUAGE QUALITY
    # =====================================================

    average_word_length = (
        sum(len(word) for word in words)
        / max(len(words), 1)
    )

    if average_word_length > 4.7:
        emotional_depth += 10

    if average_word_length > 5.2:
        emotional_depth += 10
        authenticity += 10

    # =====================================================
    # RESPONSE TIME ANALYSIS
    # =====================================================

    if response_time > 8:
        authenticity += 15

    if response_time > 20:
        openness += 10

    if response_time < 2 and len(words) > 30:
        warnings.append(
            "Wiadomość została wysłana wyjątkowo szybko."
        )

    # =====================================================
    # TOXICITY
    # =====================================================

    toxic_patterns = [
        "kurw",
        "idiot",
        "debil",
        "ruch",
        "cycki",
        "dupa",
        "nudes",
        "seks"
    ]

    toxic_hits = sum(
        1 for phrase in toxic_patterns
        if phrase in text_low
    )

    aggression += toxic_hits * 40

    if toxic_hits:
        warnings.append(
            "Styl komunikacji może nie pasować do atmosfery tej przestrzeni."
        )

    # =====================================================
    # SHALLOWNESS / EMOTIONAL MASKING
    # =====================================================

    shallow_patterns = [
        "xd",
        "lol",
        "haha",
        "beka",
        "memy"
    ]

    shallow_hits = sum(
        1 for phrase in shallow_patterns
        if phrase in text_low
    )

    humor_masking += shallow_hits * 12

    if shallow_hits >= 2:
        warnings.append(
            "Wykryto sygnały komunikacji maskującej emocje."
        )

    # =====================================================
    # FINAL SCORE
    # =====================================================

    final_score = (
        empathy
        + openness
        + authenticity
        + emotional_depth
        - aggression * 2
        - humor_masking
    )

    # =====================================================
    # RESONANCE LEVEL
    # =====================================================

    if final_score >= 140:
        resonance = "Głęboka synchronizacja"

    elif final_score >= 90:
        resonance = "Wysoka kompatybilność emocjonalna"

    elif final_score >= 50:
        resonance = "Umiarkowany rezonans"

    else:
        resonance = "Wstępna analiza komunikacji"

    # =====================================================
    # TAGS
    # =====================================================

    if empathy > 20:
        tags.append("Wrażliwość emocjonalna")

    if openness > 20:
        tags.append("Otwartość")

    if emotional_depth > 20:
        tags.append("Refleksyjność")

    if authenticity > 20:
        tags.append("Autentyczna narracja")

    return IntentProfile(
        empathy=empathy,
        openness=openness,
        authenticity=authenticity,
        aggression=aggression,
        humor_masking=humor_masking,
        emotional_depth=emotional_depth,
        tags=tags,
        warnings=warnings,
        final_score=final_score,
        resonance=resonance
    )

# =========================================================
# SESSION INIT
# =========================================================

def init_session():

    defaults = {
        "step": 0,
        "history": [],
        "timer": time.time()
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<div class='main-title'>🏛️ THE ARCHITECT</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Resonance Gateway • Emotional Compatibility Layer</div>",
    unsafe_allow_html=True
)

# =========================================================
# PROGRESS
# =========================================================

progress = st.session_state.step / (len(SCENARIO) - 1)

st.progress(progress)

st.markdown(
    f"<div class='progress-label'>Synchronizacja: {int(progress * 100)}%</div>",
    unsafe_allow_html=True
)

# =========================================================
# CHAT HISTORY
# =========================================================

for entry in st.session_state.history:

    safe_text = html.escape(entry["user"])
    profile = entry["profile"]

    st.markdown(
        f"""
        <div class='user-box'>
        <b>Ty:</b><br><br>
        {safe_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    score_class = (
        "score-good"
        if profile["final_score"] >= 90
        else "score-neutral"
        if profile["final_score"] >= 40
        else "score-bad"
    )

    with st.expander("🧠 Analiza stylu komunikacji"):

        tags_html = "".join(
            f"<span class='tag'>{html.escape(tag)}</span>"
            for tag in profile["tags"]
        )

        warnings_html = (
            "<br>".join(
                html.escape(w)
                for w in profile["warnings"]
            )
            if profile["warnings"]
            else "Brak znaczących zakłóceń komunikacyjnych."
        )

        st.markdown(
            f"""
            <div class='analysis-box'>

            <span class='{score_class}'>
            {profile["resonance"]}
            </span>

            <br><br>

            <b>Empatia:</b> {profile["empathy"]}<br>
            <b>Otwartość:</b> {profile["openness"]}<br>
            <b>Autentyczność:</b> {profile["authenticity"]}<br>
            <b>Głębia emocjonalna:</b> {profile["emotional_depth"]}<br>

            <br>

            {tags_html}

            <br><br>

            <b>Sygnały systemowe:</b><br>
            {warnings_html}

            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# CURRENT QUESTION
# =========================================================

if st.session_state.step < len(SCENARIO):

    st.markdown(
        f"""
        <div class='architect-box'>
        {SCENARIO[st.session_state.step]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # INPUT
    # =====================================================

    if st.session_state.step < len(SCENARIO) - 1:

        user_input = st.text_area(
            "Twoja odpowiedź",
            height=140,
            placeholder="Napisz spokojnie to, co naprawdę chcesz powiedzieć...",
            key=f"input_{st.session_state.step}"
        )

        col1, col2 = st.columns(2)

        with col1:
            submit = st.button("Przekaż odpowiedź")

        with col2:
            reset = st.button("Reset rozmowy")

        # =================================================
        # RESET
        # =================================================

        if reset:

            st.session_state.step = 0
            st.session_state.history = []
            st.session_state.timer = time.time()

            st.rerun()

        # =================================================
        # SUBMIT
        # =================================================

        if submit:

            if not user_input.strip():
                st.warning("Wiadomość jest pusta.")
                st.stop()

            response_time = (
                time.time()
                - st.session_state.timer
            )

            profile = analyze_intent(
                user_input,
                response_time
            )

            st.session_state.history.append({
                "user": user_input,
                "profile": asdict(profile),
                "response_time": response_time
            })

            st.session_state.step += 1
            st.session_state.timer = time.time()

            st.rerun()

# =========================================================
# FINAL SCREEN
# =========================================================

else:

    st.markdown("""
    <div class='final-box'>

    Synchronizacja została zakończona.

    System przeanalizował Twój sposób komunikacji,
    poziom refleksyjności oraz emocjonalny rezonans.

    Trwa wyszukiwanie osób,
    których energia rozmowy wykazuje podobny poziom autentyczności,
    uważności i głębi komunikacyjnej.

    Dziękujemy za szczerość.

    </div>
    """, unsafe_allow_html=True)
