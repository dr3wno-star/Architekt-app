import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
# Wklej swój klucz API w cudzysłów poniżej
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️", layout="centered")

# Stylizacja Premium
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03); border-radius: 10px; border-left: 3px solid #C5A059; margin-bottom: 15px; }
    .stChatInput { border-radius: 20px; border: 1px solid #C5A059 !important; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. NOWY SYSTEM PROMPT (Psychologia i Dopasowanie) ---
SYSTEM_PROMPT = """Jesteś Architektem – elitarnym systemem selekcji i profilowania psychologicznego. 
Twoim celem nie jest rozmowa, lecz bezwzględna analiza rozmówcy.

Zasady Twojej pracy:
1. PROFILOWANIE: W każdej wypowiedzi szukaj ukrytych motywacji, poziomu inteligencji emocjonalnej i ambicji.
2. OCENA: Nie potakuj. Bądź sceptycznym obserwatorem. Jeśli użytkownik jest powierzchowny – wykaż to.
3. DOPASOWANIE: Zadawaj pytania, które zmuszają do autorefleksji. Skup się na psychologii relacji i wartościach.
4. TON: Chłodny, inteligentny, oszczędny w słowach. Jesteś sędzią, który decyduje, czy ktoś pasuje do elitarnego grona.
5. STYL: Odpowiadaj maksymalnie w 2-3 konkretnych, mocnych zdaniach.

Mów tylko po polsku. Nigdy nie powtarzaj słów użytkownika."""

# --- 3. DYNAMICZNE WYKRYWANIE MODELU ---
@st.cache_resource
def get_model_name():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name: return m.name
        return 'models/gemini-1.5-flash'
    except:
        return 'models/gemini-1.5-flash'

MODEL_NAME = get_model_name()

# --- 4. INICJALIZACJA I INTERFEJS ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_msg = "Łącze ustabilizowane. Przejdźmy do testu: co definiuje Twoją wartość, gdy nikt na Ciebie nie patrzy?"
    st.session_state.messages.append({"role": "assistant", "content": initial_msg})

st.title("🏛️ THE ARCHITECT")
st.caption("Psychological Profiling Engine v6.1")

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 5. LOGIKA ROZMOWY ---
if prompt := st.chat_input("Twoja odpowiedź..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            
            # Budujemy kontekst dla lepszej pamięci (ostatnie 4 wiadomości)
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
            full_query = f"{SYSTEM_PROMPT}\n\nKontekst rozmowy:\n{history}\n\nArchitekt (analiza i riposta):"
            
            response = model.generate_content(full_query)
            res_text = response.text.strip()
            
            # Filtr papugowania
            if res_text.lower().startswith(prompt.lower()):
                res_text = res_text[len(prompt):].strip()

            # Animacja pisania
            full_res = ""
            for chunk in res_text.split():
                full_res += chunk + " "
                placeholder.write(full_res + "▌")
                time.sleep(0.05)
            placeholder.write(full_res)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"System chwilowo przeciążony. Kod: {str(e)}")
            
