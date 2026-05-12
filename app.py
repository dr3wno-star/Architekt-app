import streamlit as st
import html
import random
from dataclasses import dataclass
from typing import List

# =========================================================
# KONFIGURACJA
# =========================================================

st.set_page_config(
    page_title="Architekt",
    page_icon="🌙",
    layout="wide"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(65,85,120,0.18), transparent 30%),
        radial-gradient(circle at bottom right, rgba(80,90,150,0.10), transparent 35%),
        #090D12;
    color: #E7EDF5;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.main-title {
    text-align:center;
    font-size:3.2rem;
    font-weight:600;
    margin-top:20px;
    margin-bottom:8px;
}

.subtitle {
    text-align:center;
    color:#9AA8B5;
    margin-bottom:35px;
    line-height:1.8;
}

.box {
    background:linear-gradient(145deg,#121821,#0D1218);
    border:1px solid #25303A;
    border-radius:20px;
    padding:24px;
    margin-bottom:20px;
    line-height:1.9;
}

.question-box {
    border-left:4px solid #5EA8FF;
}

.user-box {
    background:#0F141B;
    border:1px solid #25303A;
    border-radius:18px;
    padding:18px;
    margin-top:15px;
}

.profile-box {
    background:linear-gradient(145deg,#10161D,#0C1016);
    border:1px solid #26313B;
    border-left:4px solid #6EE7B7;
    border-radius:20px;
    padding:28px;
    margin-top:20px;
}

.match-box {
    background:linear-gradient(145deg,#111821,#0D1218);
    border:1px solid #24303A;
    border-radius:18px;
    padding:22px;
    margin-bottom:18px;
}

.tag {
    display:inline-block;
    background:#17212C;
    color:#8FC7FF;
    padding:6px 12px;
    border-radius:999px;
    margin:4px;
    font-size:0.82rem;
}

.soft-tag {
    display:inline-block;
    background:#15201B;
    color:#7FE0B0;
    padding:6px 12px;
    border-radius:999px;
    margin:4px;
    font-size:0.82rem;
}

.stat {
    margin-bottom:10px;
}

.stButton > button {
    width:100%;
    border-radius:14px;
    background:linear-gradient(135deg,#4A8FE7,#2563C7);
    color:white;
    border:none;
    padding:0.9rem;
    font-size:1rem;
    transition:0.3s ease;
}

.stButton > button:hover {
    transform:translateY(-1px);
    box-shadow:0 8px 20px rgba(74,143,231,0.3);
}

textarea {
    border-radius:14px !important;
    background-color:#10161D !important;
    color:#E6EDF3 !important;
    border:1px solid #28313A !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PYTANIA
# =========================================================

QUESTIONS = [

    "Kiedy ostatni raz poczułeś, że możesz być całkowicie sobą przy drugim człowieku?",

    "Jakiego rodzaju rozmów najbardziej brakuje Ci w codziennym życiu?",

    "Co najbardziej męczy Cię w dzisiejszych relacjach między ludźmi?",

    "Czy łatwo przychodzi Ci mówienie o emocjach?",

    "Jak wygląda dla Ciebie poczucie bezpieczeństwa w relacji?",

    "Jak reagujesz, gdy ktoś naprawdę próbuje Cię zrozumieć?"
]

# =========================================================
# ARCHETYPY
# =========================================================

ARCHETYPES = {

    "Nocny Myśliciel": {
        "desc":
            "Osoba introspektywna, analizująca emocje i relacje głębiej niż większość ludzi.",
        "style":
            "Powolne, refleksyjne rozmowy i emocjonalna autentyczność."
    },

    "Ciche Serce": {
        "desc":
            "Wrażliwa osoba, która potrzebuje bezpieczeństwa i spokojnej obecności.",
        "style":
            "Delikatna komunikacja, cierpliwość i emocjonalna uważność."
    },

    "Obserwator": {
        "desc":
            "Najpierw słucha i analizuje, zanim się otworzy.",
        "style":
            "Spokojna komunikacja i głębokie budowanie zaufania."
    },

    "Wędrowiec": {
        "desc":
            "Człowiek szukający swojego miejsca i prawdziwego połączenia.",
        "style":
            "Poszukiwanie emocjonalnej bliskości i zrozumienia."
    },

    "Głębia": {
        "desc":
            "Silna potrzeba autentycznych i bardzo głębokich rozmów.",
        "style":
            "Intensywne połączenia emocjonalne i wysoka refleksyjność."
    }
}

# =========================================================
# DANE DEMO
# =========================================================

MATCHES = [

    {
        "name": "Alicja",
        "age": 26,
        "archetype": "Ciche Serce",
        "distance": "12 km",
        "bio":
            "Lubi spokojne wieczory, długie rozmowy i ludzi, przy których nie trzeba nic udawać.",
        "tags":
            ["Spokojna energia", "Empatia", "Slow bonding"]
    },

    {
        "name": "Maja",
        "age": 28,
        "archetype": "Nocny Myśliciel",
        "distance": "31 km",
        "bio":
            "Najbardziej ceni szczerość, emocjonalną dojrzałość i poczucie bezpieczeństwa.",
        "tags":
            ["Refleksyjność", "Nocne rozmowy", "Introwertyzm"]
    },

    {
        "name": "Natalia",
        "age": 25,
        "archetype": "Obserwator",
        "distance": "18 km",
        "bio":
            "Nie lubi pośpiechu. Potrzebuje czasu, aby poczuć prawdziwe połączenie.",
        "tags":
            ["Powolne relacje", "Spokój", "Uważność"]
    }
]

# =========================================================
# MODEL
# =========================================================

@dataclass
class Profile:

    empathy: int
    reflection: int
    vulnerability: int
    calmness: int
    emotional_depth: int
    loneliness: int

    archetype: str

    tags: List[str]

# =========================================================
# ANALIZA
# =========================================================

def analyze_answers(answers):

    combined = " ".join(answers).lower()

    empathy = 0
    reflection = 0
    vulnerability = 0
    calmness = 0
    emotional_depth = 0
    loneliness = 0

    tags = []

    empathy_words = [
        "rozumiem", "czuję", "empatia",
        "bliskość", "emocje", "wrażliwość",
        "zrozumienie", "wsparcie", "obecność"
    ]

    reflection_words = [
        "zastanawiam", "myślę",
        "mam wrażenie", "analizuję",
        "czasami", "od dawna"
    ]

    vulnerability_words = [
        "boję się", "trudno mi",
        "ukrywam", "nie radzę sobie",
        "samotny", "samotna"
    ]

    calm_words = [
        "spokój", "cisza",
        "bezpieczeństwo", "harmonia"
    ]

    loneliness_words = [
        "sam", "pustka",
        "brakuje mi", "izolacja"
    ]

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
        emotional_depth += 40

    if empathy > 20:
        tags.append("Empatia")

    if reflection > 20:
        tags.append("Refleksyjność")

    if vulnerability > 20:
        tags.append("Otwartość emocjonalna")

    if calmness > 20:
        tags.append("Potrzeba spokoju")

    if emotional_depth > 30:
        tags.append("Głębia rozmowy")

    archetype = "Wędrowiec"

    if reflection > 40:
        archetype = "Nocny Myśliciel"

    if calmness > 30:
        archetype = "Ciche Serce"

    if emotional_depth > 60:
        archetype = "Głębia"

    return Profile(
        empathy,
        reflection,
        vulnerability,
        calmness,
        emotional_depth,
        loneliness,
        archetype,
        tags
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
    "<div class='main-title'>🌙 THE ARCHITECT</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    Przestrzeń dla spokojnych, autentycznych rozmów.<br>
    Bez swipe'ów. Bez presji. Bez udawania.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FLOW
# =========================================================

if not st.session_state.finished:

    progress = st.session_state.step / len(QUESTIONS)

    st.progress(progress)

    current_question = QUESTIONS[st.session_state.step]

    st.markdown(
        f"""
        <div class='box question-box'>
        {current_question}
        </div>
        """,
        unsafe_allow_html=True
    )

    user_input = st.text_area(
        "Twoja odpowiedź",
        height=160,
        placeholder="Nie musisz się spieszyć.",
        key=f"question_{st.session_state.step}"
    )

    col1, col2 = st.columns(2)

    with col1:
        next_btn = st.button("Kontynuuj")

    with col2:
        reset_btn = st.button("Reset")

    if reset_btn:

        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.finished = False

        st.rerun()

    if next_btn:

        if not user_input.strip():
            st.warning("Wpisz odpowiedź.")
            st.stop()

        st.session_state.answers.append(user_input)

        if st.session_state.step < len(QUESTIONS) - 1:
            st.session_state.step += 1
        else:
            st.session_state.finished = True

        st.rerun()

# =========================================================
# ETAP PO ANALIZIE
# =========================================================

else:

    profile = analyze_answers(
        st.session_state.answers
    )

    left, right = st.columns([1.1, 1])

    # =====================================================
    # PROFIL EMOCJONALNY
    # =====================================================

    with left:

        tags_html = "".join(
            f"<span class='tag'>{tag}</span>"
            for tag in profile.tags
        )

        st.markdown(
            f"""
            <div class='profile-box'>

            <h2>{profile.archetype}</h2>

            <i>{ARCHETYPES[profile.archetype]["desc"]}</i>

            <hr>

            <b>Styl komunikacji:</b><br>
            {ARCHETYPES[profile.archetype]["style"]}

            <br><br>

            <div class='stat'>
            Empatia • {profile.empathy}
            </div>

            <div class='stat'>
            Refleksyjność • {profile.reflection}
            </div>

            <div class='stat'>
            Otwartość emocjonalna • {profile.vulnerability}
            </div>

            <div class='stat'>
            Potrzeba spokoju • {profile.calmness}
            </div>

            <div class='stat'>
            Głębia emocjonalna • {profile.emotional_depth}
            </div>

            <div class='stat'>
            Potrzeba bliskości • {profile.loneliness}
            </div>

            <br>

            {tags_html}

            <hr>

            System wykrył zwiększoną potrzebę
            autentycznej komunikacji,
            spokojnych relacji
            oraz emocjonalnego bezpieczeństwa.

            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # MATCHING
    # =====================================================

    with right:

        st.markdown("""
        <div class='box'>
        <h3>Potencjalne połączenia</h3>

        System nie dopasowuje ludzi na podstawie zdjęć,
        lecz stylu komunikacji i emocjonalnego rezonansu.
        </div>
        """, unsafe_allow_html=True)

        for match in MATCHES:

            tags = "".join(
                f"<span class='soft-tag'>{tag}</span>"
                for tag in match["tags"]
            )

            st.markdown(
                f"""
                <div class='match-box'>

                <h4>{match["name"]}, {match["age"]}</h4>

                <b>Archetyp:</b> {match["archetype"]}<br>
                <b>Odległość:</b> {match["distance"]}

                <br><br>

                {match["bio"]}

                <br><br>

                {tags}

                </div>
                """,
                unsafe_allow_html=True
            )

        st.button("Rozpocznij spokojną rozmowę")

    # =====================================================
    # DODATKOWE TRYBY
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    mode1, mode2, mode3 = st.columns(3)

    with mode1:

        st.markdown("""
        <div class='box'>

        <h4>🌙 Nocne rozmowy</h4>

        Połączenia aktywne po 22:00.
        Więcej refleksyjnych i spokojnych osób.

        </div>
        """, unsafe_allow_html=True)

    with mode2:

        st.markdown("""
        <div class='box'>

        <h4>☁️ Slow bonding</h4>

        Brak zdjęć przez pierwsze 24h rozmowy.
        Najpierw komunikacja.

        </div>
        """, unsafe_allow_html=True)

    with mode3:

        st.markdown("""
        <div class='box'>

        <h4>🎧 Voice atmosphere</h4>

        Delikatne ambientowe pokoje głosowe.
        Bez kamer. Bez presji.

        </div>
        """, unsafe_allow_html=True)
