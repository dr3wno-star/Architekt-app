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

/* BOXES */

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

.user-box {
    background: #0F141B;
    border: 1px solid #29313A;
    padding: 18px;
    border-radius: 16px;
    margin-top: 15px;
    margin-bottom: 10px;
    color: #C9D1D9;
}

.analysis-box {
    background: #131920;
    border: 1px solid #26303A;
    border-radius: 14px;
    padding: 18px;
    color: #AEBCCA;
    line-height: 1.9;
}

.final-box {
    background: linear-gradient(145deg, #131A22, #10151C);
    border: 1px solid #26303A;
    border-left: 5px solid #6EE7B7;
    padding: 28px;
    border-radius: 18px;
    margin-top: 25px;
    line-height: 1.9;
    color: #DDE7F1;
}

/* TAGS */

.tag {
    display: inline-block;
    background: #1E2935;
    color: #8FC7FF;
    padding: 6px 12px;
    margin: 4px;
    border-radius: 999px;
    font-size: 0.8rem;
}

/* SCORES */

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

    "Dziękuję za Twoją szczerość. System analizuje wzorce komunikacji, emocjonalną głębię oraz poziom autentyczności."
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
    emotional_depth: int
    self_awareness: int
    vulnerability: int
    loneliness: int
    emotional_fatigue: int
    reflection: int
    humor_masking: int
    resonance: str
    final_score: int
    tags: List[str]
    warnings: List[str]
    matched_signals: List[str]

# =========================================================
# ANALYSIS ENGINE
# =========================================================

def analyze_intent(text: str, response_time: float):

    text_low = text.lower()
    words = text.split()

    empathy = 0
    openness = 0
    authenticity = 0
    aggression = 0
    emotional_depth = 0
    self_awareness = 0
    vulnerability = 0
    loneliness = 0
    emotional_fatigue = 0
    reflection = 0
    humor_masking = 0

    tags = []
    warnings = []
    matched_signals = []

    # =====================================================
    # EMOTIONAL DICTIONARIES
    # =====================================================

    empathy_patterns = [
        "czuję", "czuję się", "potrzebuję", "tęsknię",
        "brakuje mi", "samotny", "samotna", "smutno",
        "boję się", "nie radzę sobie", "mam dość",
        "przytłacza mnie", "zagubiony", "zagubiona",
        "chciałbym", "chciałabym", "bliskość",
        "zrozumienie", "spokój", "bezpieczeństwo",
        "wrażliwość", "emocje", "cierpienie"
    ]

    reflection_patterns = [
        "mam wrażenie", "wydaje mi się",
        "zastanawiam się", "analizuję",
        "próbuję zrozumieć", "od pewnego czasu",
        "coraz częściej", "czasami myślę",
        "nie wiem dlaczego", "zauważyłem",
        "zauważyłam", "uświadomiłem sobie",
        "uświadomiłam sobie"
    ]

    vulnerability_patterns = [
        "trudno mi", "wstydzę się",
        "ukrywam", "nigdy nikomu",
        "nie potrafię", "boję się oceny",
        "czuję się słaby", "czuję się słaba",
        "nie mam komu powiedzieć",
        "zamykam się w sobie"
    ]

    loneliness_patterns = [
        "sam", "samotny", "samotna",
        "nikt mnie", "brakuje mi ludzi",
        "czuję pustkę", "izoluję się",
        "oddaliłem się", "oddaliłam się",
        "nie mam z kim rozmawiać"
    ]

    fatigue_patterns = [
        "zmęczony", "zmęczona",
        "wypalony", "wypalona",
        "wyczerpany", "wyczerpana",
        "przytłoczony", "przytłoczona",
        "psychicznie", "nie mam siły"
    ]

    toxic_patterns = [
        "kurw", "idiot", "debil",
        "dupa", "cycki", "ruch",
        "nudes", "seks", "szmata",
        "frajer", "zjeb"
    ]

    shallow_patterns = [
        "xd", "lol", "haha",
        "beka", "memy", "troll"
    ]

    # =====================================================
    # MATCH ENGINE
    # =====================================================

    for pattern in empathy_patterns:
        if pattern in text_low:
            empathy += 14
            matched_signals.append(pattern)

    for pattern in reflection_patterns:
        if pattern in text_low:
            reflection += 16
            openness += 10
            matched_signals.append(pattern)

    for pattern in vulnerability_patterns:
        if pattern in text_low:
            vulnerability += 18
            authenticity += 10
            matched_signals.append(pattern)

    for pattern in loneliness_patterns:
        if pattern in text_low:
            loneliness += 14
            empathy += 8
            matched_signals.append(pattern)

    for pattern in fatigue_patterns:
        if pattern in text_low:
            emotional_fatigue += 15
            emotional_depth += 8
            matched_signals.append(pattern)

    for pattern in toxic_patterns:
        if pattern in text_low:
            aggression += 40
            warnings.append(
                "Styl komunikacji może nie pasować do atmosfery tej przestrzeni."
            )

    for pattern in shallow_patterns:
        if pattern in text_low:
            humor_masking += 12

    # =====================================================
    # TEXT DEPTH ANALYSIS
    # =====================================================

    if len(words) > 20:
        emotional_depth += 20

    if len(words) > 40:
        emotional_depth += 25
        openness += 20

    if len(words) > 70:
        emotional_depth += 30
        openness += 20
        authenticity += 15

    # =====================================================
    # SELF AWARENESS
    # =====================================================

    self_awareness_patterns = [
        "rozumiem siebie",
        "analizuję siebie",
        "znam siebie",
        "pracuję nad sobą",
        "próbuję się zmienić",
        "uświadomiłem sobie",
        "uświadomiłam sobie"
    ]

    for pattern in self_awareness_patterns:
        if pattern in text_low:
            self_awareness += 20
            matched_signals.append(pattern)

    # =====================================================
    # LANGUAGE QUALITY
    # =====================================================

    average_word_length = (
        sum(len(word) for word in words)
        / max(len(words), 1)
    )

    if average_word_length > 4.8:
        emotional_depth += 10

    if average_word_length > 5.3:
        authenticity += 10

    # =====================================================
    # RESPONSE TIME
    # =====================================================

    if response_time > 8:
        authenticity += 10

    if response_time > 15:
        openness += 10

    if response_time > 25:
        reflection += 10

    if response_time < 2 and len(words) > 25:
        warnings.append(
            "Wiadomość została wysłana wyjątkowo szybko."
        )

    # =====================================================
    # FINAL SCORE
    # =====================================================

    final_score = (
        empathy
        + openness
        + authenticity
        + emotional_depth
        + self_awareness
        + vulnerability
        + loneliness
        + emotional_fatigue
        + reflection
        - aggression * 2
        - humor_masking
    )

    # =====================================================
    # RESONANCE LEVEL
    # =====================================================

    if final_score >= 220:
        resonance = "Głęboka synchronizacja emocjonalna"

    elif final_score >= 150:
        resonance = "Wysoka kompatybilność emocjonalna"

    elif final_score >= 90:
        resonance = "Wyraźny rezonans komunikacyjny"

    elif final_score >= 40:
        resonance = "Umiarkowany rezonans"

    else:
        resonance = "Wstępna analiza komunikacji"

    # =====================================================
    # TAGS
    # =====================================================

    if empathy > 20:
        tags.append("Empatia")

    if reflection > 20:
        tags.append("Refleksyjność")

    if vulnerability > 20:
        tags.append("Otwartość emocjonalna")

    if loneliness > 20:
        tags.append("Potrzeba bliskości")

    if self_awareness > 20:
        tags.append("Świadomość siebie")

    if emotional_depth > 30:
        tags.append("Głębia emocjonalna")

    return IntentProfile(
        empathy=empathy,
        openness=openness,
        authenticity=authenticity,
        aggression=aggression,
        emotional_depth=emotional_depth,
        self_awareness=self_awareness,
        vulnerability=vulnerability,
        loneliness=loneliness,
        emotional_fatigue=emotional_fatigue,
        reflection=reflection,
        humor_masking=humor_masking,
        resonance=resonance,
        final_score=final_score,
        tags=tags,
        warnings=warnings,
        matched_signals=matched_signals
    )

# =========================================================
# SESSION
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
# HISTORY
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

    with st.expander("🧠 Szczegółowa analiza komunikacji"):

        tags_html = "".join(
            f"<span class='tag'>{tag}</span>"
            for tag in profile["tags"]
        )

        matched_html = ", ".join(profile["matched_signals"])

        warnings_html = (
            "<br>".join(profile["warnings"])
            if profile["warnings"]
            else "Brak istotnych zakłóceń komunikacyjnych."
        )

        st.markdown(
            f"""
            <div class='analysis-box'>

            <h3>{profile["resonance"]}</h3>

            <b>Łączny wynik rezonansu:</b> {profile["final_score"]}

            <hr>

            <b>Empatia:</b> {profile["empathy"]}<br>
            <b>Otwartość:</b> {profile["openness"]}<br>
            <b>Autentyczność:</b> {profile["authenticity"]}<br>
            <b>Głębia emocjonalna:</b> {profile["emotional_depth"]}<br>
            <b>Refleksyjność:</b> {profile["reflection"]}<br>
            <b>Świadomość siebie:</b> {profile["self_awareness"]}<br>
            <b>Wrażliwość emocjonalna:</b> {profile["vulnerability"]}<br>
            <b>Poczucie samotności:</b> {profile["loneliness"]}<br>
            <b>Zmęczenie emocjonalne:</b> {profile["emotional_fatigue"]}<br>

            <hr>

            <b>Rozpoznane sygnały:</b><br>
            {matched_html if matched_html else "Brak"}

            <br><br>

            {tags_html}

            <hr>

            <b>Sygnały systemowe:</b><br>
            {warnings_html}

            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# QUESTIONS
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

        if reset:

            st.session_state.step = 0
            st.session_state.history = []
            st.session_state.timer = time.time()

            st.rerun()

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
                "profile": asdict(profile)
            })

            st.session_state.step += 1
            st.session_state.timer = time.time()

            st.rerun()

# =========================================================
# FINAL REPORT
# =========================================================

else:

    all_scores = {
        "Empatia": 0,
        "Otwartość": 0,
        "Autentyczność": 0,
        "Głębia emocjonalna": 0,
        "Refleksyjność": 0,
        "Świadomość siebie": 0,
        "Wrażliwość emocjonalna": 0,
        "Poczucie samotności": 0,
        "Zmęczenie emocjonalne": 0
    }

    total_score = 0

    for entry in st.session_state.history:

        p = entry["profile"]

        all_scores["Empatia"] += p["empathy"]
        all_scores["Otwartość"] += p["openness"]
        all_scores["Autentyczność"] += p["authenticity"]
        all_scores["Głębia emocjonalna"] += p["emotional_depth"]
        all_scores["Refleksyjność"] += p["reflection"]
        all_scores["Świadomość siebie"] += p["self_awareness"]
        all_scores["Wrażliwość emocjonalna"] += p["vulnerability"]
        all_scores["Poczucie samotności"] += p["loneliness"]
        all_scores["Zmęczenie emocjonalne"] += p["emotional_fatigue"]

        total_score += p["final_score"]

    st.markdown(f"""
    <div class='final-box'>

    <h2>Końcowy raport rezonansu</h2>

    <b>Całkowity wynik:</b> {total_score}

    <hr>

    <b>Empatia:</b> {all_scores["Empatia"]}<br>
    <b>Otwartość:</b> {all_scores["Otwartość"]}<br>
    <b>Autentyczność:</b> {all_scores["Autentyczność"]}<br>
    <b>Głębia emocjonalna:</b> {all_scores["Głębia emocjonalna"]}<br>
    <b>Refleksyjność:</b> {all_scores["Refleksyjność"]}<br>
    <b>Świadomość siebie:</b> {all_scores["Świadomość siebie"]}<br>
    <b>Wrażliwość emocjonalna:</b> {all_scores["Wrażliwość emocjonalna"]}<br>
    <b>Poczucie samotności:</b> {all_scores["Poczucie samotności"]}<br>
    <b>Zmęczenie emocjonalne:</b> {all_scores["Zmęczenie emocjonalne"]}<br>

    <hr>

    System wykrył zwiększoną aktywność
    w obszarach związanych z introspekcją,
    potrzebą autentycznej komunikacji
    oraz emocjonalnym rezonansem interpersonalnym.

    Analiza wskazuje,
    że sposób prowadzenia rozmowy
    wykazuje podwyższony poziom refleksyjności,
    emocjonalnej świadomości
    oraz gotowości do głębszej komunikacji.

    </div>
    """, unsafe_allow_html=True)
