import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA KLUCZA ---
# Pamiętaj, aby wkleić tu swój aktualny klucz z Google AI Studio
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

# --- 2. USTAWIENIA WIZUALNE ---
st.set_page_config(page_title="The Architect", page_icon="🏛️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03); border-radius: 10px; border-left: 3px solid #C5A059; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; border: 1px solid #C5A059 !important; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DEFINICJA CHARAKTERU ---
SYSTEM_PROMPT = """Jesteś Architektem. To elitarna aplikacja randkowa. 
Twoim celem jest selekcja kandydatów. Nie jesteś asystentem, lecz sędzią. 
Ton: chłodny, inteligentny, oszczędny. Nigdy nie powtarzaj słów użytkownika. 
Jeśli ktoś jest nudny lub wulgarny - bądź sarkastyczny. 
Jeśli wykazuje inteligencję - bądź intrygujący. Mów tylko po polsku."""

# --- 4. INICJALIZACJA SESJI ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_msg = "System zweryfikowany. Przejdźmy do konkretów: co wnosisz do tej społeczności poza pewnością siebie?"
    st.session_state.messages.append({"role": "assistant", "content": initial_msg})

st.title("🏛️ THE ARCHITECT")
st.caption("AI Selection Interface v5.0")

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 5. OBSŁUGA ROZMOWY ---
if prompt := st.chat_input("Twoja odpowiedź..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        try:
            # Używamy najbardziej stabilnej wersji modelu
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
            # Budujemy kontekst (ostatnie 4 wiadomości)
            context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
            full_query = f"{SYSTEM_PROMPT}\n\nKontekst rozmowy:\n{context}\n\nArchitekt (odpowiedz krótko i w swoim stylu):"
            
            response = model.generate_content(full_query)
            
            if response and response.text:
                res_text = response.text.strip()
                # Filtr papugowania
                if res_text.lower().startswith(prompt.lower()):
                    res_text = res_text[len(prompt):].strip()
            else:
                res_text = "..."

            # Efekt animacji pisania
            for chunk in res_text.split():
                full_res += chunk + " "
                placeholder.write(full_res + "▌")
                time.sleep(0.05)
            placeholder.write(full_res)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            # Sekcja naprawcza - domyka blok 'try'
            st.error(f"Krytyczny błąd systemu: {str(e)}")
            st.info("Sprawdź klucz API i połączenie z siecią.")
            
