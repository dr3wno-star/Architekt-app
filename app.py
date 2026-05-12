import streamlit as st
import time
import html
from dataclasses import dataclass, asdict
from typing import List, Dict

# =========================================================
# CONFIG
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

/* TEXTAREA */

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

/* ANIM */

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

    "Dziękuję za Twoją szczerość. System analizuje styl komunikacji, aby dopasować Cię do osób o podobnej energii rozmowy."
]

# =========================================================
# ANALYSIS ENGINE
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


def analyze_intent(text: str, response_time: float) -> IntentProfile:

    text_low = text.lower()

    empathy_patterns = [
        "czuję", "potrzebuję", "samot", "smut",
        "boję", "tęsk", "spokój", "rozum",
        "blisko", "cisza", "zagub"
    ]

    openness_patterns = [
        "nigdy nikomu", "trudno mi", "ukrywam",
        "mam wrażenie", "czasami", "nie wiem",
        "od dawna"
    ]

    toxic_patterns = [
        "kurw", "idiot", "debil", "nudes",
        "seks", "ruch", "dupa", "cycki"
    ]

    shallow_patterns = [
        "xd", "lol", "haha", "beka",
        "troll", "memy"
    ]

    empathy = 0
    openness = 0
    authenticity = 0
    aggression = 0
    humor_masking = 0
    emotional_depth = 0

    tags = []
    warnings = []

    # =========================================
    # EMPATHY
    # =========================================

    empathy_hits = sum(
        1 for pattern in empathy_patterns
        if pattern in text_low
    )

    empathy += empathy_hits * 12

    if empathy_hits >= 2:
        tags.append("Wrażliwość emocjonalna")

    # =========================================
    # OPENNESS
    # =========================================

    openness_hits = sum(
        1 for pattern in openness_patterns
        if pattern in text_low
    )

    openness += openness_hits * 15

    if len(text.split()) > 25:
        openness += 20
        emotional_depth += 15
        tags.append("Gotowość do otwarcia się")

    # =========================================
    # AUTHENTICITY
    # =========================================

    avg_word_length = sum(len(w) for w in text.split()) / max(len(text.split()), 1)

    if avg_word_length > 4:
        authenticity += 20

    if response_time > 8:
        authenticity += 10

    # =========================================
    # TOXICITY
    # =========================================

    toxic_hits = sum(
        1 for pattern in toxic_patterns
        if pattern in text_low
    )

    aggression += toxic_hits * 35

    if toxic_hits:
        warnings.append("Styl komunikacji może zakłócać atmosferę tej przestrzeni.")

    # =========================================
    # SHALLOW / MASKING
    # =========================================

    shallow_hits = sum(
        1 for pattern in shallow_patterns
        if pattern in text_low
    )

    humor_masking += shallow_hits * 10

    if shallow_hits >= 2:
        warnings.append("Wykryto sygnały komunikacji maskującej emocje.")

    # =========================================
    # IMPULSIVE DETECTION
    # =========================================

    if response_time < 3 and len(text.split()) > 20:
        warnings.append("Wypowiedź została wysłana bardzo szybko.")

    # =========================================
    # FINAL SCORE
    # =========================================

    final_score = (
        empathy * 2
        + openness
        + authenticity
        + emotional_depth
        - aggression * 2
        - humor_masking
    )

    return IntentProfile(
        empathy=empathy,
        openness=openness,
        authenticity=authenticity,
        aggression=aggression,
        humor_masking=humor_masking,
        emotional_depth=emotional_depth,
        tags=tags,
        warnings=warnings,
        final_score=final_score
    )

# =========================================================
# SESSION
# =========================================================

def init_session():
    defaults = {
        "step": 0,
        "history": [],
        "timer": time.time(),
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

    safe_user_text = html.escape(entry["user"])

    st.markdown(
        f"""
        <div class='user-box'>
        <b>Ty:</b><br><br>
        {safe_user_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    profile = entry["profile"]

    score_class = (
        "score-good"
        if profile["final_score"] >= 80
        else "score-neutral"
        if profile["final_score"] >= 20
        else "score-bad"
    )

    with st.expander("🧠 Analiza stylu komunikacji"):

        tags_html = "".join(
            [f"<span class='tag'>{html.escape(tag)}</span>" for tag in profile["tags"]]
        )

        warnings_html = "<br>".join(
            [html.escape(w) for w in profile["warnings"]]
        ) or "Brak znaczących zakłóceń komunikacyjnych."

        st.markdown(
            f"""
            <div class='analysis-box'>

            <span class='{score_class}'>
            Wynik rezonansu: {profile["final_score"]}
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
# CURRENT STEP
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
            placeholder="Napisz spokojnie to, co naprawdę chcesz powiedzieć..."
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            submit = st.button("Przekaż odpowiedź")

        with col2:
            clear = st.button("Wyczyść")

        if clear:
            st.rerun()

        if submit:

            if not user_input.strip():
                st.warning("Wiadomość jest pusta.")
                st.stop()

            response_time = time.time() - st.session_state.timer

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

    st.success(
        "Synchronizacja zakończona pomyślnie."
    )

    st.markdown("""
    <div class='architect-box'>
    Twój styl komunikacji został przeanalizowany.

    System poszukuje teraz osób,
    których sposób prowadzenia rozmowy
    wykazuje podobny poziom otwartości,
    refleksyjności i emocjonalnego rezonansu.

    Dziękujemy za autentyczność.
    </div>
    """, unsafe_allow_html=True)

    st.balloons()
