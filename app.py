import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1); }
    .report-box { background-color: #1A1A1B; border: 1px solid #C5A059; padding: 15px; border-radius: 10px; color: #C5A059; font-size: 0.85rem; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELIGENTNE WYKRYWANIE MODELU ---
@st.cache_resource
def find_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            # Szukamy flash, potem pro, a jak nie ma to bierzemy pierwszy z brzegu
            for name in available_models:
                if '1.5-flash' in name: return name
            for name in available_models:
                if 'pro' in name: return name
            return available_models[0]
    except Exception as e:
        st.error(f"Nie udało się pobrać listy modeli: {str(e)}")
    return None

WORKING_MODEL = find_working_model()

# --- 3. SYSTEM PROMPT ---
SYSTEM_PROMPT = """Jesteś 'Architektem'. Rozmawiaj jak normalny, konkretny człowiek. 
Po znaku '###' napisz krótką analizę psychologiczną rozmówcy dla Konrada."""

# --- 4. INTERFEJS ---
st.title("🏛️ THE ARCHITECT")

if not WORKING_MODEL:
    st.error("Klucz API nie ma dostępu do żadnych modeli. Sprawdź status klucza w Google AI Studio.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System gotowy. O czym pogadamy?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if "###" in content:
            msg, report = content.split("###")
            st.write(msg.strip())
            with st.expander("👁️ RAPORT"):
                st.markdown(f"<div class='report-box'>{report.strip()}</div>", unsafe_allow_html=True)
        else:
            st.write(content)

if user_input := st.chat_input("Napisz..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(WORKING_MODEL)
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-3:]])
            full_query = f"{SYSTEM_PROMPT}\n\nHistoria:\n{history}\n\nUżytkownik: {user_input}\nArchitekt:"
            
            response = model.generate_content(full_query)
            res_full = response.text
            
            if "###" in res_full:
                u_text, r_text = res_full.split("###")
                st.write(u_text.strip())
                with st.expander("👁️ RAPORT"):
                    st.markdown(f"<div class='report-box'>{r_text.strip()}</div>", unsafe_allow_html=True)
            else:
                st.write(res_full)
            st.session_state.messages.append({"role": "assistant", "content": res_full})
            
        except Exception as e:
            st.error(f"Błąd przy modelu {WORKING_MODEL}: {str(e)}")
            
