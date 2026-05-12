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

# --- 2. SYSTEM PROMPT ---
SYSTEM_PROMPT = """Jesteś 'Architektem'. Rozmawiaj naturalnie i konkretnie. 
Po znaku '###' napisz krótką analizę psychologiczną rozmówcy dla Konrada."""

# --- 3. FUNKCJA GENERUJĄCA (Z PEŁNĄ DIAGNOSTYKĄ) ---
def generate_architect_response(prompt_text):
    try:
        # Próbujemy najpierw najnowszego modelu flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Budujemy kontekst z historii sesji
        history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-3:]])
        full_query = f"{SYSTEM_PROMPT}\n\nHistoria:\n{history}\n\nUżytkownik: {prompt_text}\nArchitekt:"
        
        response = model.generate_content(full_query)
        return response.text
    except Exception as e:
        # Zwracamy surowy błąd do wyświetlenia
        return f"ERROR_DIAG: {str(e)}"

# --- 4. INTERFEJS ---
st.title("🏛️ THE ARCHITECT")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System aktywny. O czym chcesz porozmawiać?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if "###" in content:
            msg, report = content.split("###")
            st.write(msg.strip())
            with st.expander("👁️ ANALIZA"):
                st.markdown(f"<div class='report-box'>{report.strip()}</div>", unsafe_allow_html=True)
        else:
            st.write(content)

if user_input := st.chat_input("Napisz..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        res_full = generate_architect_response(user_input)
        
        if "ERROR_DIAG:" in res_full:
            st.error(f"Wykryto problem z połączeniem Google API:")
            st.code(res_full.replace("ERROR_DIAG: ", ""))
            st.info("Jeśli widzisz 'User location is not supported', musisz zmienić region w ustawieniach Streamlit Cloud na USA.")
        else:
            if "###" in res_full:
                u_text, r_text = res_full.split("###")
                st.write(u_text.strip())
                with st.expander("👁️ ANALIZA"):
                    st.markdown(f"<div class='report-box'>{r_text.strip()}</div>", unsafe_allow_html=True)
            else:
                st.write(res_full)
            st.session_state.messages.append({"role": "assistant", "content": res_full})
            
