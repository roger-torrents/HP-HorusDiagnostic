import streamlit as st
import requests
import time

# --- CONFIGURATION ---
# Recorda que si ja has publicat el workflow, hauries de fer servir la URL de producció (sense el "-test")
N8N_URL = "https://rogertorrents.app.n8n.cloud/webhook-test/eaab8f5c-d748-4631-aae8-4ec8fef933cd" 
HP_BLUE = "#007DB8"
HP_DARK_BLUE = "#005A87"
HP_LIGHT_BLUE = "#E6F2F8"

st.set_page_config(
    page_title="HP Horus Smart Support", 
    page_icon="🤖", 
    layout="centered"
)

# --- PROFESSIONAL CSS ---
st.markdown(f"""
    <style>
    /* Estil general */
    .stApp {{ background-color: #ffffff; }}
    @import url('https://fonts.googleapis.com/css2?family=Hammersmith+One&display=swap');

    /* Capçalera */
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 20px 0;
        border-bottom: 3px solid {HP_BLUE};
        margin-bottom: 30px;
    }}
    .main-title {{
        color: {HP_BLUE};
        font-family: 'Hammersmith One', sans-serif;
        font-size: 32px;
        margin: 0;
    }}
    
    /* Targetes de selecció */
    div.stButton > button {{
        border: 2px solid {HP_BLUE};
        border-radius: 12px;
        color: {HP_BLUE};
        background-color: white;
        height: 100px;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    div.stButton > button:hover {{
        background-color: {HP_LIGHT_BLUE};
        border-color: {HP_DARK_BLUE};
        transform: translateY(-2px);
    }}
    
    /* Botons d'acció */
    .stButton > button[kind="primary"] {{
        background-color: {HP_BLUE} !important;
        color: white !important;
        height: 50px !important;
        font-size: 18px !important;
    }}

    /* Estil del missatge de la IA */
    .ai-response {{
        background-color: {HP_LIGHT_BLUE};
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid {HP_BLUE};
        margin-top: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'pas' not in st.session_state:
    st.session_state.pas = 1
if 'dades' not in st.session_state:
    st.session_state.dades = {}

# --- HEADER ---
st.markdown(f"""
    <div class="header-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/HP_logo_2012.svg" width="60">
        <h1 class="main-title">HORUS SMART SUPPORT</h1>
    </div>
""", unsafe_allow_html=True)

# --- STEP 1: PROBLEM SELECTION ---
if st.session_state.pas == 1:
    st.subheader("🛠️ Select the issue you are experiencing")
    st.write("Diagnostic system ready. Please identify the primary symptom:")
    
    col1, col2 = st.columns(2)
    
    options = [
        {"icon": "🔌", "label": "Does not turn on", "context": "Power issue", "type": "foto"},
        {"icon": "📄", "label": "Printing errors", "context": "Printing issue", "type": "foto"},
        {"icon": "❌", "label": "Poor print quality", "context": "Quality issue", "type": "foto"},
        {"icon": "🔊", "label": "Strange noises", "context": "Mechanical noise", "type": "audio"}
    ]

    for i, opt in enumerate(options):
        with col1 if i % 2 == 0 else col2:
            if st.button(f"{opt['icon']} {opt['label']}", key=opt['label']):
                st.session_state.dades.update({'problema': opt['context'], 'input': opt['type']})
                st.session_state.pas = 2
                st.rerun()

# --- STEP 2: DYNAMIC INPUT ---
elif st.session_state.pas == 2:
    input_type = st.session_state.dades['input']
    context_text = st.session_state.dades['problema']
    
    st.caption(f"Support > Diagnostic > {context_text}")
    st.progress(0.6)

    with st.container():
        st.info(f"📍 **Current Case:** {context_text}")

        fitxer = None
        if input_type == 'foto':
            st.markdown("### 📸 **Visual Evidence**")
            st.write("Please capture the error code, lights, or the affected area.")
            fitxer = st.camera_input("Capture image")
        else:
            st.markdown("### 🎤 **Acoustic Analysis**")
            st.write("Record the sound for at least 5 seconds while the device is in operation.")
            fitxer = st.audio_input("Record sound")

        if fitxer:
            if st.button("🚀 ANALYZE WITH HORUS AI", type="primary", use_container_width=True):
                with st.status("HP Horus AI is analyzing the data...", expanded=True) as status:
                    try:
                        files = {"file": (fitxer.name, fitxer.getvalue(), fitxer.type)}
                        data = {"context": context_text}
                        
                        response = requests.post(N8N_URL, files=files, data=data)
                        
                        if response.status_code == 200:
                            status.update(label="Analysis Finished!", state="complete", expanded=False)
                            st.session_state.resposta = response.text
                            st.session_state.pas = 3
                            st.rerun()
                        else:
                            st.error(f"Error: Server returned status {response.status_code}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
    
    if st.button("⬅️ Back to Menu"):
        st.session_state.pas = 1
        st.rerun()

# --- STEP 3: RESULTS ---
elif st.session_state.pas == 3:
    st.progress(1.0)
    st.success("✅ **Diagnostic Completed Successfully**")
    
    # Presentació de la resposta de la IA amb estil HP
    st.markdown(f"""
        <div class="ai-response">
            <h3 style="color: {HP_DARK_BLUE}; margin-top: 0;">HP Expert Recommendation:</h3>
            {st.session_state.resposta}
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🔄 Start New Diagnostic", use_container_width=True):
        st.session_state.pas = 1
        st.rerun()

# FOOTER
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: #888;'>
        <small>© 2026 HP Enterprise Support Services<br>
        AI System: Horus 2.0 | Status: Operational</small>
    </div>
""", unsafe_allow_html=True)
