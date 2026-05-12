import streamlit as st
import google.generativeai as genai
import time

# --- KONFIGURACJA ---
API_KEY = "AIzaSyBl0o-YNjRcjGeu3E362FRtPFkVIaSesjs"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️")

# Stylizacja Premium
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03); border-radius: 10px; border-left: 3px solid #C5A059; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE ARCHITECT")

# --- LOGIKA SYSTEMU ---
SYSTEM_PROMPT = """Jesteś Architektem. To elitarna aplikacja randkowa. 
Twoim celem jest bezwzględna selekcja. Nie jesteś asystentem. 
Jesteś sędzią. Twój ton: chłodny, inteligentny, oszczędny w słowach. 
Nigdy nie powtarzaj słów użytkownika. Jeśli ktoś jest nudny - skróć rozmowę.
Jeśli ktoś wykazuje wysoką inteligencję - bądź intrygujący. 
Mów tylko po polsku."""

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Powitanie startowe
    initial_msg = "System zweryfikowany. Przejdźmy do konkretów: co wnosisz do tej społeczności poza pewnością siebie?"
    st.session_state.messages.append({"role": "assistant", "content": initial_msg})

# Wyświetlanie historii
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obsługa wejścia
if prompt := st.chat_input("Napisz..."):
    # Dodajemy wiadomość użytkownika do widoku
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Budujemy kontekst: System Prompt + ostatnie 4 wiadomości dla pamięci
            history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
            full_query = f"{SYSTEM_PROMPT}\n\nHistoria:\n{history_context}\n\nArchitekt:"
            
            response = model.generate_content(full_query)
            res_text = response.text.strip()
            
            # Naprawa błędu "papugowania" - jeśli AI powtarza użytkownika, czyścimy to
            if res_text.lower().startswith(prompt.lower()):
                res_text = res_text[len(prompt):].strip()

            # Efekt pisania
            full_res = ""
            for chunk in res_text.split():
                full_res += chunk + " "
                placeholder.write(full_res + "▌")
                time.sleep(0.05)
            placeholder.write(full_res)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"Autoryzacja przerwana. Spróbuj ponownie.")
            
