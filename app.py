import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA MÓZGU (AI) ---
# Upewnij się, że klucz jest poprawny i aktywny w Google AI Studio
API_KEY = "AIzaSyBl0o-YNjRcjGeu3E362FRtPFkVIaSesjs" 
genai.configure(api_key=API_KEY)

# Instrukcja charakteru bota
SYSTEM_PROMPT = """
Jesteś 'Architektem' - inteligentnym, chłodnym botem elitarnej aplikacji. 
Twoim zadaniem jest rozmowa, aby wybadać status i inteligencję rozmówcy.
Zasady:
- Nie bądź miły. Bądź konkretny i profesjonalny.
- Jeśli ktoś trolluje - bądź sarkastyczny.
- Jeśli ktoś pisze o celach (dom, rodzina, biznes) - drąż temat.
- Rozmawiaj po polsku.
"""

# Używamy formatu, który omija błąd 404 w większości regionów
model = genai.GenerativeModel('gemini-pro')

# --- 2. KONFIGURACJA WYGLĄDU (UI) ---
st.set_page_config(page_title="The Architect", page_icon="🏛️")

st.markdown("""
    <style>
    .stApp { background-color: #1A1A1B; color: #C5A059; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(197, 160, 89, 0.2); }
    .stChatInput { border-color: #C5A059 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE ARCHITECT")
st.caption("System Weryfikacji Tożsamości v5.0")

# --- 3. LOGIKA CZATU ---
if "messages" not in st.session_state:
    # Inicjalizacja historii z instrukcją systemową jako ukrytą wiadomością
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    # Wysyłamy instrukcję jako pierwszy komunikat, by ustawić zachowanie
    try:
        st.session_state.chat.send_message(SYSTEM_PROMPT)
    except:
        pass # Ignorujemy błąd inicjalizacji, jeśli model jest oporny
    
    st.session_state.messages.append({"role": "assistant", "content": "Cześć. Nie lubię tracić czasu. Powiedz mi, co sprawia, że jesteś ciekawszy od tysięcy innych ludzi w tej sieci?"})

# Wyświetlanie historii (pomijamy techniczne instrukcje)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obsługa wejścia użytkownika
if prompt := st.chat_input("Twoja odpowiedź..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        
        try:
            # Próba uzyskania odpowiedzi
            response = st.session_state.chat.send_message(prompt)
            
            # Efekt pisania na żywo
            for chunk in response.text.split():
                full_res += chunk + " "
                placeholder.write(full_res + "▌")
                time.sleep(0.05)
            placeholder.write(full_res)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Jeśli nadal występuje błąd, wyświetlamy go w sposób czytelny
            st.error(f"Architekt chwilowo niedostępny. Błąd: {str(e)}")
            if "404" in str(e):
                st.info("WSKAZÓWKA: Google nie widzi modelu. Spróbuj zmienić linię 25 na: model = genai.GenerativeModel('gemini-pro')")
                
