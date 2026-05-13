import streamlit as st
import random

# =========================================================
# 1. INICJALIZACJA SESJI (MUSI BYĆ NA POCZĄTKU)
# =========================================================

if "step" not in st.session_state:
    st.session_state.step = 0

if "scores" not in st.session_state:
    st.session_state.scores = {"PRAGMATYK": 0, "STRAZNIK": 0, "DUCH": 0, "WEDROWIEC": 0}

# =========================================================
# 2. BAZA WYNIKÓW
# =========================================================

AURA_DEFINITIONS = {
    "PRAGMATYK": {
        "tytul": "Aura Stalowa (Pragmatyk)",
        "opis": "Twoja energia jest konkretna i osadzona w materii. Nie marnujesz sił na iluzje. Budujesz świat z faktów i logiki. Jesteś fundamentem, na którym inni mogą polegać, ale rzadko pozwalasz sobie na słabość.",
        "pytanie": "Czy w pogoni za skutecznością nie zgubiłeś radości z samego procesu?"
    },
    "STRAZNIK": {
        "tytul": "Aura Dębowa (Strażnik)",
        "opis": "Twoja aura jest ciężka, stara i nasiąknięta historią. Jesteś jak dębowy mebel w opuszczonym domu – przetrwałeś wiele, a kurz tylko dodaje Ci szlachetności. Cenisz lojalność i trwałość ponad wszystko.",
        "pytanie": "Kogo wpuścisz za swoje ciężkie, dębowe drzwi?"
    },
    "DUCH": {
        "tytul": "Aura Eteryczna (Duch)",
        "opis": "Jesteś jak mgła lub płomień świecy. Widzisz to, czego inni nie dostrzegają. Twoja wrażliwość jest Twoją największą siłą, ale też Twoim przekleństwem. Żyjesz w świecie symboli i przeczuć.",
        "pytanie": "Jak bardzo boisz się rozproszenia przez zbyt silne światło rzeczywistości?"
    },
    "WEDROWIEC": {
        "tytul": "Aura Złota (Wędrowiec)",
        "opis": "Twoja energia jest w ciągłym ruchu. Jesteś ciepłem zachodzącego słońca i ciekawością dziecka. Szukasz relacji i głębokich połączeń z ludźmi, ale Twoja natura jest zmienna i trudna do uchwycenia.",
        "pytanie": "Gdzie jest Twoje miejsce, gdy gasną wszystkie światła?"
    }
}

# =========================================================
# 3. BAZA PYTAŃ
# =========================================================

QUESTIONS_DATABASE = [
    {
        "pytanie": "Gdy budzisz się w nocy i panuje absolutna cisza, co słyszysz?",
        "opcje": [
            ("Pracę urządzeń i szum miasta.", "PRAGMATYK"),
            ("Bicie własnego serca.", "STRAZNIK"),
            ("Ciężar powietrza i pustkę pokoju.", "DUCH"),
            ("Oddech kogoś bliskiego.", "WEDROWIEC"),
            ("Echo myśli, których nie wypowiedziałem.", "DUCH"),
            ("Nic, po prostu czekam na sen.", "PRAGMATYK")
        ]
    },
    {
        "pytanie": "Wybierz materiał, z którego mogłaby być zbudowana Twoja tarcza:",
        "opcje": [
            ("Hartowana stal – chłodna i pewna.", "PRAGMATYK"),
            ("Ciemne, surowe drewno – dębowe i silne.", "STRAZNIK"),
            ("Gęsta mgła – nieuchwytna.", "DUCH"),
            ("Złoto – cenna i plastyczna.", "WEDROWIEC"),
            ("Kamień – niewzruszony.", "STRAZNIK"),
            ("Przezroczyste szkło – dystans.", "PRAGMATYK")
        ]
    },
    {
        "pytanie": "Jakie światło najlepiej definiuje Twój obecny stan?",
        "opcje": [
            ("Ostre, biurowe światło.", "PRAGMATYK"),
            ("Płomień pojedynczej świecy.", "STRAZNIK"),
            ("Księżycowa poświata.", "DUCH"),
            ("Ciepły blask zachodzącego słońca.", "WEDROWIEC"),
            ("Światło tuż przed burzą.", "DUCH"),
            ("Zimne, niebieskie światło ekranu.", "PRAGMATYK")
        ]
    }
]

# =========================================================
# 4. DESIGN I LOGIKA
# =========================================================

st.set_page_config(page_title="SZEPT", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@100;300&display=swap');
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #050505 !important; color: #d1d1d1; }
    .question-title { font-family: 'Bodoni Moda', serif; font-size: 2rem; text-align: center; margin-top: 50px; margin-bottom: 40px; color: #fff; font-style: italic; }
    .stButton>button { background-color: #0a0a0a; border: 1px solid #222; color: #888; width: 100%; text-align: left; padding: 15px 25px; margin-bottom: 10px; font-family: 'Inter', sans-serif; transition: 0.4s; }
    .stButton>button:hover { border-color: #555; color: #fff; transform: translateX(5px); }
    .result-title { font-family: 'Bodoni Moda', serif; font-size: 2.2rem; color: #fff; text-align: center; margin-top: 80px; }
    .result-desc { font-family: 'Inter', sans-serif; font-size: 1.1rem; text-align: center; color: #aaa; line-height: 1.8; margin: 20px 0; }
    .result-question { font-family: 'Bodoni Moda', serif; font-size: 1.5rem; color: #fff; text-align: center; font-style: italic; border-top: 1px solid #222; padding-top: 20px; }
</style>
""", unsafe_allow_html=True)

# FAZA PYTAŃ
if st.session_state.step < len(QUESTIONS_DATABASE):
    q = QUESTIONS_DATABASE[st.session_state.step]
    st.markdown(f'<div class="question-title">{q["pytanie"]}</div>', unsafe_allow_html=True)
    
    for text, archetyp in q["opcje"]:
        if st.button(text, key=f"btn_{st.session_state.step}_{text}"):
            st.session_state.scores[archetyp] += 1
            st.session_state.step += 1
            st.rerun()

# FAZA WYNIKU
elif st.session_state.step >= len(QUESTIONS_DATABASE):
    final_archetyp = max(st.session_state.scores, key=st.session_state.scores.get)
    wynik = AURA_DEFINITIONS[final_archetyp]
    
    st.markdown(f'<div class="result-title">{wynik["tytul"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-desc">{wynik["opis"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-question">{wynik["pytanie"]}</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("RESETUJ PROFIL"):
        st.session_state.clear()
        st.rerun()
