import streamlit as st
import time

# --- 1. KONFIGURACJA WIZUALNA ---
st.set_page_config(page_title="The Architect - Core", page_icon="🏛️")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .report-box { 
        background-color: #1A1A1B; border: 1px solid #C5A059; 
        padding: 15px; border-radius: 10px; color: #C5A059; 
        font-family: monospace; font-size: 0.9rem;
    }
    .user-bubble { background-color: #262730; padding: 10px; border-radius: 10px; margin: 5px 0; }
    .arch-bubble { background-color: #1A1A1B; border-left: 3px solid #C5A059; padding: 10px; border-radius: 10px; margin: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKA SCENARIUSZA (Pytania Architekta) ---
SCENARIO = [
    "Witaj. Zanim przejdziemy dalej, powiedz: co sprawia, że Twoje życie jest ciekawsze od 99% innych ludzi?",
    "Interesujące. A jak reagujesz, gdy ktoś podważa Twoje kompetencje w tym, co robisz najlepiej?",
    "Rozumiem. Ostatnie pytanie: czego szukasz w drugim człowieku – lustra czy dopełnienia?",
    "Analiza zakończona. Wyniki zostały przesłane do administratora systemu."
]

# --- 3. SILNIK ANALIZY ---
def analyze_input(text, response_time):
    score = 0
    traits = []
    
    # 1. Analiza długości (Elokwencja)
    word_count = len(text.split())
    if word_count > 20:
        score += 30
        traits.append("Wysoka Elokwencja")
    elif word_count < 5:
        score -= 10
        traits.append("Lakoniczność / Brak zaangażowania")
    
    # 2. Analiza słów kluczowych (Wartości)
    keywords = {
        "pasja": "Pasjonat", "pieniądze": "Materialista", "sukces": "Ambitny",
        "spokój": "Stabilny", "ludzie": "Empatyczny", "ja": "Egocentryk",
        "nauka": "Intelektualista", "walka": "Zdeterminowany"
    }
    for word, trait in keywords.items():
        if word in text.lower():
            score += 10
            traits.append(trait)

    # 3. Analiza czasu namysłu
    if response_time < 2:
        traits.append("Impulsywność")
    elif response_time > 10:
        traits.append("Refleksyjność / Ostrożność")

    return score, traits

# --- 4. INTERFEJS CZATU ---
st.title("🏛️ THE ARCHITECT")
st.caption("Behavioral Analysis Engine v1.0 (No-API Build)")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.chat_history = []
    st.session_state.start_time = time.time()
    st.session_state.analysis_log = []

# Wyświetlanie historii
for chat in st.session_state.chat_history:
    st.markdown(f"<div class='{chat['class']}'>{chat['content']}</div>", unsafe_allow_html=True)
    if 'report' in chat:
        with st.expander("👁️ LOG ANALITYCZNY (Tylko dla Konrada)"):
            st.markdown(f"<div class='report-box'>{chat['report']}</div>", unsafe_allow_html=True)

# Główne pytanie Architekta
if st.session_state.step < len(SCENARIO):
    current_question = SCENARIO[st.session_state.step]
    st.markdown(f"<div class='arch-bubble'><b>Architekt:</b> {current_question}</div>", unsafe_allow_html=True)
    
    if st.session_state.step < len(SCENARIO) - 1:
        user_input = st.text_input("Twoja odpowiedź...", key=f"input_{st.session_state.step}")
        
        if st.button("Wyślij", key=f"btn_{st.session_state.step}"):
            if user_input:
                # Obliczanie czasu i analiza
                end_time = time.time()
                resp_time = end_time - st.session_state.start_time
                score, traits = analyze_input(user_input, resp_time)
                
                report = f"""
                <b>PARAMETRY:</b><br>
                - Czas namysłu: {resp_time:.2f}s<br>
                - Słów: {len(user_input.split())}<br>
                - Wynik Selekcji: {score} pkt<br>
                - Wykryte cechy: {', '.join(traits)}
                """
                
                # Zapis do historii
                st.session_state.chat_history.append({
                    "class": "user-bubble", 
                    "content": f"<b>Ty:</b> {user_input}",
                    "report": report
                })
                
                st.session_state.step += 1
                st.session_state.start_time = time.time()
                st.rerun()
else:
    st.success("Test zakończony. Architekt wyda werdykt wkrótce.")
    if st.button("Zacznij od nowa"):
        st.session_state.step = 0
        st.session_state.chat_history = []
        st.rerun()
        
