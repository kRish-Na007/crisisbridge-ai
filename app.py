import streamlit as st
import json
from triage_engine import analyze_emergency_signal

# Page Setup
st.set_page_config(
    page_title="CRISISBRIDGE_AI // TERMINAL_v2.5",
    page_icon="📟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Custom Terminal CSS & Hide Sidebar
st.markdown("""
<style>
    /* Hide Streamlit Sidebar & Default Header Elements */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Terminal Dark Background & Green Matrix Typography */
    .stApp {
        background-color: #050a0e;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Force Monospace Font Across All Elements */
    h1, h2, h3, h4, h5, h6, label, p, div, span, .stMarkdown {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Terminal Input Box & Select Box Styling */
    .stTextArea textarea, div[data-baseweb="select"] > div {
        background-color: #0a121a !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        border-radius: 2px !important;
        font-family: 'Courier New', Courier, monospace !important;
        box-shadow: inset 0 0 5px rgba(0, 255, 102, 0.2);
    }

    /* Terminal Action Button */
    div.stButton > button {
        background-color: #00ff66 !important;
        color: #050a0e !important;
        font-weight: bold !important;
        border: 1px solid #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
        border-radius: 2px !important;
        letter-spacing: 1px;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #050a0e !important;
        color: #00ff66 !important;
        box-shadow: 0 0 15px #00ff66 !important;
    }

    /* Glowing Terminal Container Cards */
    .terminal-card {
        background-color: #0a121a;
        border: 1px solid #00ff66;
        padding: 15px;
        border-radius: 2px;
        margin-bottom: 15px;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.15);
    }

    .terminal-alert {
        background-color: #1a0808;
        border: 1px solid #ff3333;
        color: #ff6666 !important;
        padding: 12px;
        margin-bottom: 8px;
        border-radius: 2px;
        box-shadow: 0 0 8px rgba(255, 51, 51, 0.25);
    }

    /* Metric Cards Override */
    [data-testid="stMetricValue"] {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Terminal Header Block
# Terminal Header Block
st.markdown("""
<div class="terminal-card">
<pre style="color: #00ff66; margin:0; font-size: 10px; line-height: 1.1; overflow-x: auto;">
 ██████╗██████╗ ██╗███████╗██╗███████╗██████╗ ██████╗ ██╗██████╗  ██████╗ ███████╗   █████╗ ██╗
██╔════╝██╔══██╗██║██╔════╝██║██╔════╝██╔══██╗██╔══██╗██║██╔══██╗██╔════╝ ██╔════╝  ██╔══██╗██║
██║     ██████╔╝██║███████╗██║███████╗██████╔╝██████╔╝██║██║  ██║██║  ███╗█████╗    ███████║██║
██║     ██╔══██╗██║╚════██║██║╚════██║██╔══██╗██╔══██╗██║██║  ██║██║   ██║██╔══╝    ██╔══██╗██║
╚██████╗██║  ██║██║███████║██║███████║██████╔╝██║  ██║██║██████╔╝╚██████╔╝███████╗  ██║  ██║██║
 ╚═════╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚══════╝  ╚═╝  ╚═╝╚═╝
</pre>
<hr style="border: 0.5px solid #00ff66; margin: 10px 0;">
<div style="display: flex; justify-content: space-between;">
    <span>[ STATUS: ONLINE ]</span>
    <span>[ REASONING ENGINE: NVIDIA NEMOTRON 3.5 ]</span>
    <span>[ WEB INTEL: TAVILY ENGINE ]</span>
</div>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("### 📥 [INPUT_STREAM] :: SOS SIGNAL INGESTION")

sample_preset = st.selectbox(
    "SELECT_PRESET_BUFFER:",
    [
        "CUSTOM_INPUT",
        "SOS! Water level reaching second floor at Riverside Sector 4. 3 people trapped on roof including elderly person!",
        "Earthquake damage near City Hospital. Multiple injuries reported, road blocked by debris, fire starting!",
        "Gas leak reported near Industrial Area, block 12. Workers feeling dizzy and nauseous."
    ]
)

if sample_preset != "CUSTOM_INPUT":
    sos_input = st.text_area("RAW_TEXT_PAYLOAD:", value=sample_preset, height=100)
else:
    sos_input = st.text_area("RAW_TEXT_PAYLOAD:", placeholder="> Enter distress text, voice transcription, or social SOS feed...", height=100)

process_btn = st.button(" [> EXECUTE_TRIAGE_PROTOCOL] ", type="primary", use_container_width=True)

# Triage Results Output Block
if process_btn and sos_input.strip():
    with st.spinner("[ SYSTEM_PROCESSING ] :: Parsing payload through NVIDIA Nemotron engine..."):
        result = analyze_emergency_signal(sos_input)

    st.markdown("---")
    st.markdown("### 🎯 [OUTPUT_DISPATCH_REPORT] :: OPERATIONAL INTEL")

    #