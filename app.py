import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Stylizacja
st.markdown("<style>.stApp { background-color: #1A1A1B; color: #C5A059; }</style>", unsafe_allow_html=True)

# --- 2. DYNAMICZNE WYKRYWANIE MODELU ---
@st.cache_resource
def get_model_name():
    try:
        # Sprawdzamy co Google faktycznie nam daje
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Szukamy najpierw flash, potem pro
                if 'flash' in m.name: return m.name
                if 'pro' in m.name: return m.name
        return None
    except:
        return None

MODEL_NAME = get_model_name()

# --- 3. INTERFEJS ---
st.title("🏛️ THE ARCHITECT")

if not MODEL_NAME:
    st.error("Klucz API nie widzi żadnych modeli. Sprawdź Google AI Studio.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Połączono. Co sprawia, że jesteś wart mojego czasu?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Napisz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(f"Jesteś Architektem, chłodnym botem. Odpisz po polsku: {prompt}")
            res_text = response.text
            
            placeholder = st.empty()
            full_res = ""
            for chunk in res_text.split():
                full_res += chunk + " "
                placeholder.write(full_res + "▌")
                time.sleep(0.04)
            placeholder.write(full_res)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error(f"Błąd modelu {MODEL_NAME}: {str(e)}")
            
