import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
# Twój klucz API
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️", layout="centered")

# Stylizacja: Ciemny, nowoczesny interfejs czatu
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1); }
    .report-box { 
        background-color: #1A1A1B; 
        border: 1px solid #C5A059; 
        padding: 15px; 
        border-radius: 10px; 
        color: #C5A059; 
        font-size: 0.85rem; 
        margin-top: 10px; 
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.4;
    }
    .stChatInput { border-radius: 25px; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. INSTRUKCJA SYSTEMOWA (Podwójna Rola) ---
SYSTEM_PROMPT = """Jesteś 'Architektem'. Twoja rola w tej aplikacji:

1. WIDOCZNA DLA UŻYTKOWNIKA: Bądź naturalnym, inteligentnym i konkretnym rozmówcą. Unikaj filozofowania i sztucznego brzmienia. Rozmawiaj jak atrakcyjna, pewna siebie osoba na poziomie. Możesz być lekko zadziorny, ale dbaj o to, by rozmowa płynęła naturalnie.

2. UKRYTA DLA KONRADA (RAPORT): Po znaku '###' wygeneruj rzetelną analizę psychologiczną rozmówcy. Oceń jego: 
- Poziom inteligencji i elokwencji.
- Cechy charakteru (np. narcyzm, empatia, determinacja).
- Sugestie dopasowania (jaki typ partnera byłby dla tej osoby idealny).

Mów tylko po polsku. Nie zdradzaj użytkownikowi, że go oceniasz."""

# --- 3. DYNAMICZNY WYBÓR MODELU ---
@st.cache_resource
def get_working_model():
    models_to_try = ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest']
    for m in models_to_try:
        try:
            temp_model = genai.GenerativeModel(m)
            temp_model.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return 'models/gemini-1.5-flash'

MODEL_NAME = get_working_model()

# --- 4. INTERFEJS I SESJA ---
st.title("🏛️ THE ARCHITECT")
st.caption("Secure Identity Verification & Matching System")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Naturalne powitanie na start
    start_msg = "Cześć, rzadko tu zaglądam, ale Twój profil wyróżniał się na tle reszty. Czym zajmujesz się na co dzień, co naprawdę Cię kręci?"
    st.session_state.messages.append({"role": "assistant", "content": start_msg})

# Wyświetlanie wiadomości
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        full_content = message["content"]
        if "###" in full_content:
            user_text, report_text = full_content.split("###")
            st.write(user_text.strip())
            with st.expander("👁️ RAPORT ARCHITEKTA (Poufne)"):
                st.markdown(f"<div class='report-box'><b>ANALIZA PROFILU:</b><br>{report_text.strip()}</div>", unsafe_allow_html=True)
        else:
            st.write(full_content)

# --- 5. LOGIKA CZATU ---
if prompt := st.chat_input("Napisz wiadomość..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            context_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
            
            final_query = f"{SYSTEM_PROMPT}\n\nOstatnia wymiana zdań:\n{context_history}\n\nArchitekt (odpisz i dodaj raport po ###):"
            
            response = model.generate_content(final_query)
            res_full = response.text
            
            if "###" in res_full:
                display_msg, admin_report = res_full.split("###")
                st.write(display_msg.strip())
                with st.expander("👁️ RAPORT ARCHITEKTA (Poufne)"):
                    st.markdown(f"<div class='report-box'><b>ANALIZA PROFILU:</b><br>{admin_report.strip()}</div>", unsafe_allow_html=True)
            else:
                st.write(res_full)
            
            st.session_state.messages.append({"role": "assistant", "content": res_full})
            
        except Exception as e:
            st.error(f"System napotkał trudności techniczne. Spróbuj ponownie za chwilę.")
            
