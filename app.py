import streamlit as st
import google.generativeai as genai
import time

# --- KONFIGURACJA ---
API_KEY = "AIzaSyBl0o-YNjRcjGeu3E362FRtPFkVIaSesjs"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Stylizacja
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid #C5A059; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE ARCHITECT")

# Funkcja wybierająca działający model
def get_working_model():
    try:
        # Próbujemy najpierw standardowy model
        m = genai.GenerativeModel('gemini-1.5-flash')
        m.generate_content("test", generation_config={"max_output_tokens": 1})
        return 'gemini-1.5-flash'
    except:
        try:
            # Szukamy jakiegokolwiek modelu obsługującego generowanie treści
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    return m.name
        except:
            return None
    return 'gemini-1.5-flash'

if "model_name" not in st.session_state:
    st.session_state.model_name = get_working_model()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System gotowy. Co sprawia, że jesteś wart mojego czasu?"}]

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obsługa wejścia
if prompt := st.chat_input("Napisz coś..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        if not st.session_state.model_name:
            res_text = "Błąd: Twój klucz API nie ma dostępu do żadnego modelu generatywnego. Sprawdź Google AI Studio."
        else:
            try:
                model = genai.GenerativeModel(st.session_state.model_name)
                # Łączymy instrukcję z promptem (metoda najbezpieczniejsza)
                full_prompt = f"Jesteś Architektem, chłodnym botem. Odpisz krótko po polsku: {prompt}"
                response = model.generate_content(full_prompt)
                res_text = response.text
            except Exception as e:
                res_text = f"Nadal błąd (Model: {st.session_state.model_name}): {str(e)}"

        # Efekt pisania
        full_res = ""
        for chunk in res_text.split():
            full_res += chunk + " "
            placeholder.write(full_res + "▌")
            time.sleep(0.04)
        placeholder.write(full_res)
        st.session_state.messages.append({"role": "assistant", "content": res_text})
        
