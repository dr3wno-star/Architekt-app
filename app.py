import streamlit as st
import time

# --- 1. USTAWIENIA WIZUALNE ---
st.set_page_config(page_title="The Architect | Profiling", page_icon="🏛️")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .report-box { 
        background-color: #1A1A1B; border: 1px solid #C5A059; 
        padding: 20px; border-radius: 12px; color: #C5A059; 
        font-family: 'Courier New', monospace; font-size: 0.9rem;
        line-height: 1.5;
    }
    .arch-bubble { 
        background-color: #1A1A1B; border-left: 4px solid #C5A059; 
        padding: 15px; border-radius: 10px; margin: 15px 0;
        font-style: italic; color: #E0E0E0;
    }
    .user-bubble { 
        background-color: #262730; padding: 12px; 
        border-radius: 10px; margin: 10px 0; border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SCENARIUSZ PRZESŁUCHANIA (Pytania Behawioralne) ---
# Każde pytanie jest zaprojektowane, by uderzyć w inny obszar psychiki.
SCENARIO = [
    "Większość ludzi tylko odgrywa role. Opisz sytuację z ostatniego roku, w której musiałeś zdjąć maskę i pokazać swoją prawdziwą, niekoniecznie idealną naturę. Co to o Tobie mówi?",
    "Wyobraź sobie, że osiągasz absolutny szczyt swoich marzeń, ale ceną jest całkowita samotność. Wchodzisz w to, czy szukasz kompromisu? Uzasadnij wybór.",
    "Gdybyś miał moc usunięcia jednej cechy z ludzkiej psychiki, co by to było i dlaczego akurat to Cię tak irytuje?",
    "Analiza danych zakończona. System generuje ostateczny profil tożsamości."
]

# --- 3. ROZBUDOWANY SILNIK ANALIZY ---
def deep_profile_analysis(text, response_time):
    traits = []
    red_flags = []
    green_flags = []
    
    text_low = text.lower()
    words = text.split()
    word_count = len(words)

    # --- ANALIZA 1: SPRAWCZOŚĆ I DOMINACJA ---
    dominance_markers = ["zrobię", "osiągnąłem", "decydować", "kontrola", "wynik", "moje", "zbudowałem"]
    submission_markers = ["może", "chyba", "nie wiem", "trudno", "inni", "pewnie", "chciałbym"]
    
    dom_score = sum(1 for w in dominance_markers if w in text_low)
    sub_score = sum(1 for w in submission_markers if w in text_low)

    if dom_score > sub_score:
        traits.append("Wysoka Sprawczość (Typ Lidera)")
        green_flags.append("Bierze odpowiedzialność za narrację")
    elif sub_score > dom_score:
        traits.append("Unikanie Odpowiedzialności (Typ Reaktywny)")
        red_flags.append("Niskie poczucie kontroli nad własnym życiem")

    # --- ANALIZA 2: INTELIGENCJA EMOCJONALNA (EQ) ---
    eq_keywords = ["czuję", "zrozumiałem", "relacja", "empatia", "perspektywa", "wybaczam", "ludzie"]
    if any(w in text_low for w in eq_keywords):
        traits.append("Wysokie EQ / Świadomość Emocjonalna")
    else:
        traits.append("Niskie EQ / Chłód Analityczny")

    # --- ANALIZA 3: PROFIL WARTOŚCI ---
    if any(w in text_low for w in ["pieniądze", "prestiż", "władza", "status", "zysk"]):
        traits.append("Orientacja na Status i Zasoby")
    if any(w in text_low for w in ["prawda", "zasady", "honor", "lojalność", "etyka"]):
        traits.append("Orientacja na Kodeks Wartości")
    if any(w in text_low for w in ["wolność", "podróże", "niezależność", "wybór"]):
        traits.append("Wysoka Potrzeba Autonomii")

    # --- ANALIZA 4: STABILNOŚĆ I STRES ---
    if response_time < 2.5:
        traits.append("Impulsywność / Szybka Intuicja")
    elif response_time > 12:
        traits.append("Głęboka Refleksyjność / Ukrywanie Prawdy")

    if "..." in text or text.isupper():
        red_flags.append("Niestabilność emocjonalna / Ukryta frustracja")

    # --- ANALIZA 5: ELOKWENCJA ---
    if word_count > 30:
        green_flags.append("Zdolność do autoanalizy i bogate słownictwo")
    elif word_count < 6:
        red_flags.append("Płytkość wypowiedzi / Brak chęci do współpracy")

    return traits, red_flags, green_flags, word_count

# --- 4. INTERFEJS ---
st.title("🏛️ THE ARCHITECT")
st.caption("Advanced Behavioral & Psychological Profiling v2.0")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.history = []
    st.session_state.timer = time.time()

# Wyświetlanie czatu i raportów
for entry in st.session_state.history:
    st.markdown(f"<div class='user-bubble'><b>Kandydat:</b> {entry['user']}</div>", unsafe_allow_html=True)
    with st.expander("👁️ RAPORT Z ANALIZY"):
        st.markdown(f"""
        <div class='report-box'>
        <b>PROFIL PSYCHOLOGICZNY:</b><br>
        - Główne cechy: {', '.join(entry['traits'])}<br><br>
        <b>SYGNAŁY (FLAGS):</b><br>
        <span style='color: #4CAF50;'>🟢 GREEN:</span> {', '.join(entry['greens']) if entry['greens'] else 'Brak'}<br>
        <span style='color: #F44336;'>🔴 RED:</span> {', '.join(entry['reds']) if entry['reds'] else 'Brak'}<br><br>
        <b>DANE TECHNICZNE:</b><br>
        - Czas namysłu: {entry['time']:.2f}s | Długość: {entry['words']} słów
        </div>
        """, unsafe_allow_html=True)

# Pytanie Architekta
if st.session_state.step < len(SCENARIO):
    st.markdown(f"<div class='arch-bubble'><b>Architekt:</b> {SCENARIO[st.session_state.step]}</div>", unsafe_allow_html=True)
    
    if st.session_state.step < len(SCENARIO) - 1:
        with st.form(key=f"form_{st.session_state.step}"):
            u_input = st.text_area("Twoja odpowiedź:", height=100)
            submit = st.form_submit_button("Wyślij do weryfikacji")
            
            if submit and u_input:
                resp_t = time.time() - st.session_state.timer
                tr, rd, gr, wc = deep_profile_analysis(u_input, resp_t)
                
                st.session_state.history.append({
                    "user": u_input,
                    "traits": tr,
                    "reds": rd,
                    "greens": gr,
                    "time": resp_t,
                    "words": wc
                })
                st.session_state.step += 1
                st.session_state.timer = time.time()
                st.rerun()
else:
    st.success("Profilowanie zakończone. System dokonał kategoryzacji obiektu.")
    if st.button("Nowa sesja"):
        st.session_state.step = 0
        st.session_state.history = []
        st.rerun()
        
