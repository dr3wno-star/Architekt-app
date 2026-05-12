import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Stylizacja
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03); border-radius: 10px; border-left: 3px solid #C5A059; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELIGENTNE WYKRYWANIE MODELU ---
@st.cache_resource
def find_accessible_model():
    # Szukamy jakiegokolwiek modelu, który obsługuje generowanie tekstu
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Preferujemy flash, ale bierzemy co dają
            if '1.5-flash' in m.name:
                return m.name
            if '1.5-pro' in m.name:
                return m.name
            if 'gemini-pro' in m.name:
                return m.name
    return None

# Flash jest prawie zawsze darmowy i dostępny
MODEL_NAME = 'models/gemini-1.5-flash'


# --- 3. LOGIKA CZATU ---
SYSTEM_PROMPT = "Jesteś Architektem. Chłodny, elitarny ton. Selekcja randkowa. Mów po polsku."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System aktywny. Czego oczekujesz od elity?"}]

st.title("🏛️ THE ARCHITECT")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Twoja odpowiedź..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        if not MODEL_NAME:
            st.error("Błąd: Twoje konto Google AI nie ma przypisanych żadnych modeli. Wejdź na Google AI Studio i zaakceptuj warunki.")
        else:
                        try:
                model = genai.GenerativeModel(MODEL_NAME)
                # Krótszy prompt zużywa mniej "tokenów" (Twojego limitu)
                response = model.generate_content(
                    f"{SYSTEM_PROMPT}\nUżytkownik: {prompt}",
                    generation_config={"max_output_tokens": 100} 
                )
                res_text = response.text
                            
                
                full_res = ""
                for chunk in res_text.split():
                    full_res += chunk + " "
                    placeholder.write(full_res + "▌")
                    time.sleep(0.05)
                placeholder.write(full_res)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
                
            except Exception as e:
                st.error(f"Używany model: {MODEL_NAME}. Błąd: {str(e)}")
                
