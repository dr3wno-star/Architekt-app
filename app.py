import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SZEPT", layout="centered")

# --- TWOJE PALIWO (KLUCZ) ---
API_KEY = "AIzaSyDCmJ-nxrYU3w1MSzPNij5KYd6r1Btfbog" 

# AUTOMATYCZNE WYKRYWANIE MODELU
@st.cache_resource
def get_working_model():
    try:
        genai.configure(api_key=API_KEY)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Zwracamy pierwszą działającą nazwę (np. models/gemini-1.5-flash-8b)
                return m.name
        return None
    except:
        return None

WORKING_MODEL_NAME = get_working_model()

def szept_engine(prompt_text):
    if not WORKING_MODEL_NAME:
        return "Błąd: Twój klucz nie ma dostępu do żadnego modelu Gemini."
    
    try:
        model = genai.GenerativeModel(WORKING_MODEL_NAME)
        persona = "Jesteś tajemniczym, mrocznym dziennikiem. Odpowiadaj krótko i inteligentnie."
        response = model.generate_content(f"{persona}\n\nUżytkownik: {prompt_text}")
        return response.text
    except Exception as e:
        return f"Atrament zastyga ({str(e)})"

# --- WYGLĄD ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #d1d1d1; }
    .dziennik-text { font-family: serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 2rem; border-left: 2px solid #555; padding-left: 20px; line-height: 1.6; }
    .moje-slowa { font-style: italic; color: #888; margin-bottom: 1rem; text-align: right; padding-right: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("SZEPT")

if "chat" not in st.session_state:
    st.session_state.chat = [{"role": "assistant", "content": "Czy boisz se tego, co o Tobie wiem?"}]

# Wyświetlanie
for m in st.session_state.chat:
    if m["role"] == "assistant":
        st.markdown(f'<div class="dziennik-text">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="moje-slowa">{m["content"]} —</div>', unsafe_allow_html=True)

# Wejście
user_input = st.chat_input("Napisz...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.spinner("Szukanie atramentu..."):
        res = szept_engine(user_input)
        st.session_state.chat.append({"role": "assistant", "content": res})
    st.rerun()

# Diagnostyka na dole (widoczna tylko gdy coś jest nie tak)
if WORKING_MODEL_NAME:
    st.sidebar.write(f"Aktywny model: {WORKING_MODEL_NAME}")
else:
    st.sidebar.error("BRAK DOSTĘPNYCH MODELI")
