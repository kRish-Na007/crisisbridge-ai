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

# Inject Clean Terminal CSS (Hides Sidebar & Custom Terminal Styling)
st.markdown("""
<style>
    /* Hide Streamlit Sidebar & Default Navigation */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Terminal Dark Background & Matrix Font */
    .stApp {
        background-color: #050a0e;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Force Green Monospace Typography on Headings and Labels */
    h1, h2, h3, h4, h5, h6, label, p, .stMarkdown {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Input Fields Styling */
    .stTextArea textarea, div[data-baseweb="select"] > div {
        background-color: #0a121a !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        border-radius: 2px !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Fix Button Text Visibility: Dark Text on Bright Green Button */
    div.stButton > button {
        background-color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        border-radius: 2px !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button * {
        color: #050a0e !important;
        font-weight: bold !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 16px !important;
    }
    div.stButton > button:hover {
        background-color: #050a0e !important;
        border: 1px solid #00ff66 !important;
        box-shadow: 0 0 15px #00ff66 !important;
    }
    div.stButton > button:hover * {
        color: #00ff66 !important;
    }

    /* Terminal Container Cards */
    .terminal-card {
        background-color: #0a121a;
        border: 1px solid #00ff66;
        padding: 15px;
        border-radius: 2px;
        margin-bottom: 15px;
        box-shadow: 0 0 8px rgba(0, 255, 102, 0.2);
    }

    .terminal-alert {
        background-color: #1a0808;
        border: 1px solid #ff3333;
        color: #ff6666 !important;
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 2px;
    }

    /* Metric Value Styling */
    [data-testid="stMetricValue"] {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    [data-testid="stMetricLabel"] {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# Terminal Header Banner
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
    <span>[ ENGINE: NVIDIA NEMOTRON 3.5 ]</span>
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

process_btn = st.button("[> EXECUTE_TRIAGE_PROTOCOL]", type="primary", use_container_width=True)

# Triage Results Output Block
if process_btn and sos_input.strip():
    with st.spinner("[ SYSTEM_PROCESSING ] :: Parsing payload through NVIDIA Nemotron engine..."):
        result = analyze_emergency_signal(sos_input)

    st.markdown("---")
    st.markdown("### 🎯 [OUTPUT_DISPATCH_REPORT] :: OPERATIONAL INTEL")

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("DISASTER_TYPE", result.get("disaster_type", "UNKNOWN"))
    
    urgency = result.get("urgency_level", "UNKNOWN")
    if urgency == "CRITICAL":
        m2.error(f"URGENCY: {urgency}")
    elif urgency == "HIGH":
        m2.warning(f"URGENCY: {urgency}")
    else:
        m2.info(f"URGENCY: {urgency}")
        
    m3.metric("LOCATION", result.get("location", "UNKNOWN"))
    m4.metric("VICTIMS_COUNT", result.get("victims_count", 0))

    st.markdown("<br>", unsafe_allow_html=True)

    # Required Units & Recommended Actions
    col_a, col_b = st.columns(2)

    with col_a:
        units_html = "<h4>🚒 REQUIRED_UNITS</h4>"
        for unit in result.get("required_units", []):
            units_html += f"<p>> <strong>+ {unit}</strong></p>"
        st.markdown(f'<div class="terminal-card">{units_html}</div>', unsafe_allow_html=True)

    with col_b:
        actions_html = "<h4>📋 PROTOCOL_ACTIONS</h4>"
        for idx, action in enumerate(result.get("recommended_actions", []), 1):
            actions_html += f"<p>> <strong>{idx}. {action}</strong></p>"
        st.markdown(f'<div class="terminal-card">{actions_html}</div>', unsafe_allow_html=True)

    # Situation Brief Box
    summary_text = result.get("summary", "No summary generated.")
    st.markdown(
        f'<div class="terminal-card"><h4>📝 SITUATION_BRIEF</h4><p>{summary_text}</p></div>',
        unsafe_allow_html=True
    )

    # Tavily Web Hazard Verification Section
    hazards_html = "<h4>🌐 LIVE_WEB_INTEL & ROUTE_HAZARDS (TAVILY_ENGINE)</h4>"
    hazards = result.get("live_hazards", [])
    for snippet in hazards:
        hazards_html += f'<div class="terminal-alert">⚠️ [HAZARD_ALERT] :: {snippet}</div>'
        
    st.markdown(f'<div class="terminal-card">{hazards_html}</div>', unsafe_allow_html=True)

elif process_btn:
    st.warning("⚠️ [ERROR] :: Cannot execute triage without incoming text payload.")