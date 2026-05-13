import streamlit as st
import google.generativeai as genai
import time

# =========================================================
# 1. BAZA DANYCH AURY (SZEROKA PALETA 6 OPCJI)
# =========================================================

QUESTIONS_DATABASE = [
    {
        "pytanie": "Gdy budzisz się w nocy i panuje absolutna cisza, co słyszysz?",
        "opcje": [
            "Bicie własnego serca.",
            "Pracę urządzeń i szum miasta.",
            "Echo myśli, których nie wypowiedziałem za dnia.",
            "Ciężar powietrza i pustkę pokoju.",
            "Nic, po prostu czekam na sen.",
            "Oddech kogoś bliskiego lub obecność czegoś nieuchwytnego."
        ]
    },
    {
        "pytanie": "Wybierz materiał, z którego mogłaby być zbudowana Twoja tarcza:",
        "opcje": [
            "Hartowana stal – niezniszczalna i chłodna.",
            "Ciemne, surowe drewno – nasiąknięte historią.",
            "Przezroczyste szkło – widzę wszystko, ale nikt mnie nie dotknie.",
            "Gęsta mgła – nie można mnie zranić, bo nie można mnie trafić.",
            "Kamień – twardy, ciężki i niewzruszony.",
            "Złoto – cenna, ale miękka i podatna na odkształcenia."
        ]
    },
    {
        "pytanie": "Jakie światło najlepiej definiuje Twój obecny stan ducha?",
        "opcje": [
            "Ostre, biurowe światło – pełna koncentracja.",
            "Płomień pojedynczej świecy w dużym pomieszczeniu.",
            "Światło tuż przed burzą – fioletowe i napięte.",
            "Ciepły blask zachodzącego słońca.",
            "Księżycowa poświata, która zmienia kształty przedmiotów.",
            "Zimne, niebieskie światło ekranu."
        ]
    }
]

# =========================================================
# 2. SILNIK AI (GENERATOR REZONANSU)
# =========================================================

# TWÓJ KLUCZ API
API_KEY = "AIzaSyCs2Edq1VXPVJgiUAS01fr2j2eXaQ7tQsk"
genai.configure(api_key=API_KEY)

def szept_final_analysis(answers):
    try:
        # Próbujemy Flash, jeśli nie wyjdzie - system wyrzuci błąd do obsługi
        model = genai.GenerativeModel('gemini-1.5-flash')
        persona = (
            "Jesteś Dziennikiem Badawczym. Analizujesz aurę użytkownika na podstawie jego wyborów. "
            "Użytkownik wybrał konkretne obrazy. Twoim zadaniem jest zdefiniować jego 'częstotliwość'. "
            "Nie powtarzaj jego słów. Zinterpretuj je głęboko. Powiedz mu, kim jest w świecie cieni "
            "i zadaj jedno pytanie, które uderzy w sedno jego postawy. Max 25 słów."
        )
        profile_data = " | ".join(answers)
        response = model.generate_content(f"SYSTEM: {persona}\nPROFIL: {profile_data}")
        return response.text
    except Exception as e:
        return f"Twoja aura wymyka się definicjom. ({str(e)})"

# =========================================================
# 3. DESIGN I INTERFEJS
# =========================================================

st.set_page_config(page_title="SZEPT", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@1,400&family=Inter:wght@100;300&display=swap');
    
    #MainMenu, footer, header {visibility:hidden;}
    .stApp { background-color: #050505 !important; color: #d1d1d1; }
    
    .question-title { 
        font-family: 'Bodoni Moda', serif; font-size: 2rem; text-align: center; 
        margin-top: 50px; margin-bottom: 40px; color: #fff; font-style: italic; 
    }

    .stButton>button { 
        background-color: #0a0a0a; border: 1px solid #222; color: #888; 
        width: 100%; text-align: left; padding: 15px 25px; margin-bottom: 10px;
        font-family: 'Inter', sans-serif; font-weight: 300; transition: 0.4s;
    }
    .stButton>button:hover { 
        border-color: #555; color: #fff; background-color: #111; transform: translateX(5px);
    }
    
    .final-text {
        font-family: 'Bodoni Moda', serif; font-size: 1.6rem; text-align: center;
        color: #fff; line-height: 1.6; margin-top: 100px; animation: fadeIn 3s;
    }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- INICJALIZACJA SESJI (ZAPOBIEGA ATTRIBUTE ERROR) ---
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.analysis = None

# =========================================================
# 4. LOGIKA PROCESU
# =========================================================

# FAZA 1: TEST STATYCZNY
if st.session_state.step < len(QUESTIONS_DATABASE):
    q = QUESTIONS_DATABASE[st.session_state.step]
    st.markdown(f'<div class="question-title">{q["pytanie"]}</div>', unsafe_allow_html=True)
    
    for option in q["opcje"]:
        if st.button(option):
            st.session_state.answers.append(option)
            st.session_state.step += 1
            st.rerun()

# FAZA 2: GENEROWANIE WYNIKU PRZEZ AI
elif st.session_state.step == len(QUESTIONS_DATABASE) and st.session_state.analysis is None:
    with st.spinner(" "):
        st.session_state.analysis = szept_final_analysis(st.session_state.answers)
        st.rerun()

# FAZA 3: EKRAN KOŃCOWY
if st.session_state.analysis is not None:
    st.markdown(f'<div class="final-text">{st.session_state.analysis}</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("RESETUJ PROFIL"):
        st.session_state.clear()
        st.rerun()
