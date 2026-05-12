            
import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACJA ---
API_KEY = "AIzaSyBvbCY6LskhLftq3-lG_7iluiayXkv5NZY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Architect", page_icon="🏛️", layout="centered")

# Stylizacja na "normalny czat"
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInput { border-radius: 25px; }
    /* Styl dla raportu twórcy - ukryty/wyróżniony */
    .report-box { background-color: #1A1A1B; border: 1px solid #C5A059; padding: 10px; border-radius: 10px; color: #C5A059; font-size: 0.8rem; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PODWÓJNA INSTRUKCJA SYSTEMOWA ---
SYSTEM_PROMPT = """Jesteś 'Architektem'. Twoja rola jest dwuwarstwowa:

WARSTWA 1 (Widoczna dla użytkownika): 
Zachowuj się jak normalny, inteligentny i konkretny facet/kobieta na poziomie. Nie używaj trudnych słów. Bądź bezpośredni, czasem lekko zadziorny, ale ludzki. Nie zdradzaj, że jesteś AI ani że prowadzisz selekcję. Rozmawiaj jak na normalnym, dobrym randkowym czacie.

WARSTWA 2 (Raport dla Twórcy - Konrada):
Na końcu każdej odpowiedzi, po znaku '###RAPORT###', napisz krótką analizę psychologiczną tego użytkownika. 
Oceń: 1. Inteligencję, 2. Wiarygodność, 3. Potencjał dopasowania (do kogo by pasował). 
Ta sekcja jest widoczna TYLKO dla Konrada.

Mów tylko po polsku."""

# --- 3. LOGIKA MODELU ---
@st.cache_resource
def get_model():
    return genai.GenerativeModel('models/gemini-1.5-flash')

# --- 4. INTERFEJS ---
st.title("🏛️ THE ARCHITECT")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Start rozmowy - normalny, ludzki
    st.session_state.messages.append({"role": "assistant", "content": "Cześć, rzadko tu bywam, ale Twój profil mnie zaciekawił. Czego właściwie szukasz w tym miejscu?"})

# Wyświetlanie rozmowy
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Rozdzielamy treść dla użytkownika od raportu dla Ciebie
        content = message["content"]
        if "###RAPORT###" in content:
            display_text, report = content.split("###RAPORT###")
            st.write(display_text.strip())
            # Sekcja raportu widoczna w panelu bocznym lub specjalnym boksie
            with st.expander("👁️ RAPORT ARCHITEKTA (Tylko dla Konrada)"):
                st.markdown(f"<div class='report-box'>{report.strip()}</div>", unsafe_allow_html=True)
        else:
            st.write(content)

# Obsługa czatu
if prompt := st.chat_input("Napisz coś..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            model = get_model()
            # Pamięć rozmowy
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
            full_query = f"{SYSTEM_PROMPT}\n\nRozmowa:\n{history}\n\nArchitekt (napisz odpowiedź i raport):"
            
            response = model.generate_content(full_query)
            res_full = response.text
            
            # Wyświetlanie bez raportu w głównym dymku
            if "###RAPORT###" in res_full:
                user_view, admin_report = res_full.split("###RAPORT###")
                st.write(user_view.strip())
                with st.expander("👁️ RAPORT ARCHITEKTA (Tylko dla Konrada)"):
                    st.markdown(f"<div class='report-box'>{admin_report.strip()}</div>", unsafe_allow_html=True)
            else:
                st.write(res_full)
                
            st.session_state.messages.append({"role": "assistant", "content": res_full})
            
        except Exception as e:
            st.error("Błąd połączenia.")
            
