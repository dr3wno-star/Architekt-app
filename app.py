import streamlit as st
import time
import random
import html
from dataclasses import dataclass, asdict
from typing import List

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="The Architect",
    page_icon="🌙",
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
        radial-gradient(circle at top left, rgba(71,98,130,0.15), transparent 30%),
        radial-gradient(circle at bottom right, rgba(120,120,180,0.08), transparent 35%),
        #090D12;

    color: #E8EEF5;
}

/* Hide streamlit elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* HEADER */

.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 10px;
    letter-spacing: 1px;
}

.hero-subtitle {
    text-align: center;
    color: #93A4B4;
    margin-bottom: 40px;
    line-height: 1.8;
}

/* MESSAGE BOXES */

.architect-box {
    background: linear-gradient(145deg, #121821, #0D1218);
    border: 1px solid #24303B;
    border-left: 4px solid #5DA9FF;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 25px;
    line-height: 1.9;
    animation: fadeIn 0.5s ease;
}

.user-box {
    background: #0F141B;
    border: 1px solid #222C36;
    padding: 18px;
    border-radius: 16px;
    margin-top: 15px;
    margin-bottom: 10px;
    color: #D8E1EA;
}

/* PROFILE */

.profile-box {
    background: linear-gradient(145deg, #11161D, #0D1218);
    border: 1px solid #26313C;
    border-radius: 18px;
    padding: 24px;
    margin-top: 20px;
    line-height: 1.9;
}

/* TAGS */

.tag {
    display: inline-block;
    background: #17212C;
    color: #8EC7FF;
    padding: 6px 12px;
    margin: 4px;
    border-radius: 999px;
    font-size: 0.8rem;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    background: linear-gradient(135deg, #4A8FE7, #2563C7);
    color: white;
    border: none;
    padding: 0.9rem;
    font-size: 1rem;
    font-weight: 500;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(74,143,231,0.3);
}

/* TEXT AREA */

textarea {
    border-radius: 14px !important;
    background-color: #10161D !important;
    color: #E6EDF3 !important;
    border: 1px solid #28313A !important;
}

/* FINAL */

.final-box {
    background: linear-gradient(145deg, #10161D, #0B1016);
    border: 1px solid #24303B;
    border-left: 4px solid #6EE7B7;
    padding: 28px;
    border-radius: 18px;
    margin-top: 20px;
    line-height: 1.9;
}

/* ANIMATION */

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# QUESTIONS
# =========================================================

QUESTIONS = [

    "Kiedy ostatni raz poczułeś, że naprawdę możesz być sobą przy drugim człowieku?",

    "Jak wygląda rodzaj rozmowy, którego najbardziej Ci brakuje?",

    "Co męczy Cię najbardziej w dzisiejszych relacjach między ludźmi?",

    "Czy łatwo przychodzi Ci otwieranie się emocjonalnie?",

    "Jak reagujesz, gdy ktoś naprawdę próbuje Cię zrozumieć?",

]

# =========================================================
# ARCHETYPES
# =========================================================

ARCHETYPES = {
    "The Listener":
        "Osoba spokojna, uważna i cierpliwa. Bardziej słucha niż mówi.",

    "The Deep Diver":
        "Silna potrzeba autentycznych i głębokich rozmów.",

    "The Quiet Mind":
        "Introwertyczna energia, ostrożność i refleksyjność.",

    "The Wanderer":
        "Człowiek szukający swojego miejsca i emocjonalnego bezpieczeństwa.",

    "The Night Thinker":
        "Duża introspekcja, analizowanie emocji i samotne przemyślenia.",

    "The Soft Heart":
        "Wysoka empatia i emocjonalna wrażliwość."
}

# =========================================================
# PROFILE MODEL
# =========================================================

@dataclass
class EmotionalProfile:
    empathy: int
    reflection: int
    vulnerability: int
    emotional_depth: int
    loneliness: int
    calmness: int
    authenticity: int
    archetype: str
    communication_style: str
    tags: List[str]

# =========================================================
# ANALYZER
# =========================================================

def analyze_user(texts: List[str]):

    combined = " ".join(texts).lower()

    empathy = 0
    reflection = 0
    vulnerability = 0
    emotional_depth = 0
    loneliness = 0
    calmness = 0
    authenticity = 0

    tags = []

    empathy_words = [
        "rozumiem", "czuję", "bliskość",
        "spokój", "empatia", "wrażliwość",
        "zrozumienie", "emocje"
    ]

    reflection_words = [
        "zastanawiam", "analizuję",
        "mam wrażenie", "myślę",
        "czasami", "od dawna"
    ]

    vulnerability_words = [
        "trudno mi", "boję się",
        "ukrywam", "samotny",
        "nie potrafię", "wstydzę"
    ]

    calm_words = [
        "cisza", "spokój",
        "spokojnie", "harmonia",
        "bezpieczeństwo"
    ]

    loneliness_words = [
        "sam", "samotność",
        "pustka", "izolacja",
        "brakuje mi"
    ]

    # =========================================
    # ANALYSIS
    # =========================================

    for word in empathy_words:
        if word in combined:
            empathy += 15

    for word in reflection_words:
        if word in combined:
            reflection += 18

    for word in vulnerability_words:
        if word in combined:
            vulnerability += 20

    for word in calm_words:
        if word in combined:
            calmness += 15

    for word in loneliness_words:
        if word in combined:
            loneliness += 15

    word_count = len(combined.split())

    if word_count > 80:
        emotional_depth += 35

    if word_count > 140:
        emotional_depth += 35
        authenticity += 25

    if reflection > 30:
        tags.append("Refleksyjność")

    if empathy > 20:
        tags.append("Empatia")

    if vulnerability > 20:
        tags.append("Otwartość emocjonalna")

    if calmness > 20:
        tags.append("Potrzeba spokoju")

    if loneliness > 20:
        tags.append("Potrzeba bliskości")

    # =========================================
    # ARCHETYPE
    # =========================================

    archetype = "The Wanderer"

    if reflection > 40 and emotional_depth > 40:
        archetype = "The Night Thinker"

    if empathy > 30:
        archetype = "The Soft Heart"

    if calmness > 30:
        archetype = "The Quiet Mind"

    if emotional_depth > 60:
        archetype = "The Deep Diver"

    # =========================================
    # COMMUNICATION STYLE
    # =========================================

    if emotional_depth > 60:
        style = "Slow Deep Talk"

    elif calmness > 20:
        style = "Quiet Emotional Bonding"

    else:
        style = "Reflective Communication"

    return EmotionalProfile(
        empathy=empathy,
        reflection=reflection,
        vulnerability=vulnerability,
        emotional_depth=emotional_depth,
        loneliness=loneliness,
        calmness=calmness,
        authenticity=authenticity,
        archetype=archetype,
        communication_style=style,
        tags=tags
    )

# =========================================================
# SESSION
# =========================================================

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.finished = False

# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<div class='hero-title'>🌙 THE ARCHITECT</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='hero-subtitle'>
    A calm space for authentic conversations.<br>
    No swipes. No pressure. No performance.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HISTORY
# =========================================================

for answer in st.session_state.answers:

    safe_text = html.escape(answer)

    st.markdown(
        f"""
        <div class='user-box'>
        {safe_text}
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# QUESTIONS FLOW
# =========================================================

if not st.session_state.finished:

    current_question = QUESTIONS[st.session_state.step]

    st.markdown(
        f"""
        <div class='architect-box'>
        {current_question}
        </div>
        """,
        unsafe_allow_html=True
    )

    user_input = st.text_area(
        "Your response",
        height=140,
        placeholder="Write slowly. There is no rush here.",
        key=f"question_{st.session_state.step}"
    )

    col1, col2 = st.columns(2)

    with col1:
        send = st.button("Continue")

    with col2:
        reset = st.button("Reset")

    # =========================================
    # RESET
    # =========================================

    if reset:

        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.finished = False

        st.rerun()

    # =========================================
    # CONTINUE
    # =========================================

    if send:

        if not user_input.strip():
            st.warning("Your response is empty.")
            st.stop()

        st.session_state.answers.append(user_input)

        if st.session_state.step < len(QUESTIONS) - 1:
            st.session_state.step += 1

        else:
            st.session_state.finished = True

        st.rerun()

# =========================================================
# FINAL PROFILE
# =========================================================

else:

    profile = analyze_user(
        st.session_state.answers
    )

    tags_html = "".join(
        f"<span class='tag'>{tag}</span>"
        for tag in profile.tags
    )

    st.markdown(
        f"""
        <div class='final-box'>

        <h2>{profile.archetype}</h2>

        <i>{ARCHETYPES[profile.archetype]}</i>

        <hr>

        <b>Communication Style:</b><br>
        {profile.communication_style}

        <br><br>

        <b>Detected emotional patterns:</b><br><br>

        • Empathy: {profile.empathy}<br>
        • Reflection: {profile.reflection}<br>
        • Vulnerability: {profile.vulnerability}<br>
        • Emotional Depth: {profile.emotional_depth}<br>
        • Need for Closeness: {profile.loneliness}<br>
        • Calmness Orientation: {profile.calmness}<br>

        <br>

        {tags_html}

        <hr>

        The system detected a communication style
        focused on emotional authenticity,
        calm interaction
        and deeper conversational bonding.

        Potential matches will prioritize:
        emotional safety,
        patience,
        reflective communication
        and low-pressure interaction.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "No profile photos are shown yet. "
        "Connection begins through conversation."
    )
