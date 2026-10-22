import streamlit as st
import json
from triage_engine import analyze_emergency_signal

# Page Setup
st.set_page_config(
    page_title="CrisisBridge AI",
    page_icon="🚨",
    layout="wide"
)

# Header
st.title("🚨 CrisisBridge AI — Emergency Triage Dispatch Center")
st.caption("Powered by NVIDIA Nemotron-4 on Nebius AI Cloud & Token Factory")

st.markdown("---")

# Sidebar Status
with st.sidebar:
    st.header("System Status")
    st.status("System Active (Mock Mode)", state="running")
    st.info("💡 Real-time Nebius API integration ready to hook up as soon as credits arrive.")

# Main Input Section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📥 Incoming SOS Message / Distress Signal")
    sample_preset = st.selectbox(
        "Load Sample SOS Preset:",
        [
            "Custom Input",
            "SOS! Water level reaching second floor at Riverside Sector 4. 3 people trapped on roof including elderly person!",
            "Earthquake damage near City Hospital. Multiple injuries reported, road blocked by debris, fire starting!",
            "Gas leak reported near Industrial Area, block 12. Workers feeling dizzy and nauseous."
        ]
    )

    if sample_preset != "Custom Input":
        sos_input = st.text_area("Emergency Text Signal:", value=sample_preset, height=120)
    else:
        sos_input = st.text_area("Emergency Text Signal:", placeholder="Paste incoming emergency text, tweet, or transcribed voice call...", height=120)

    process_btn = st.button("🚨 Analyze Signal & Triage", type="primary", use_container_width=True)

# Triage Results Display
if process_btn and sos_input.strip():
    with st.spinner("Processing signal through NVIDIA Nemotron reasoning engine..."):
        result = analyze_emergency_signal(sos_input)

    st.markdown("---")
    st.subheader("🎯 Intelligence & Dispatch Report")

    # Metric Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Disaster Type", result.get("disaster_type", "Unknown"))
    
    # Color badge for urgency
    urgency = result.get("urgency_level", "UNKNOWN")
    if urgency == "CRITICAL":
        m2.error(f"Urgency: {urgency}")
    elif urgency == "HIGH":
        m2.warning(f"Urgency: {urgency}")
    else:
        m2.info(f"Urgency: {urgency}")
        
    m3.metric("Location", result.get("location", "Unknown"))
    m4.metric("Victims Reported", result.get("victims_count", 0))

    st.markdown("---")

    # Operational Details
    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.write("### 🚒 Required Dispatch Units")
        for unit in result.get("required_units", []):
            st.markdown(f"- ✅ **{unit}**")

    with d_col2:
        st.write("### 📋 Recommended Actions")
        for idx, action in enumerate(result.get("recommended_actions", []), 1):
            st.markdown(f"{idx}. {action}")

    st.write("### 📝 Situation Brief")
    st.info(result.get("summary", "No summary generated."))

    # Live Hazard Verification Section (Tavily Track)
    st.markdown("---")
    st.write("### 🌐 Live Web Intelligence & Route Hazards (Powered by Tavily)")
    hazards = result.get("live_hazards", [])
    for snippet in hazards:
        st.warning(f"⚠️ {snippet}")

elif process_btn:
    st.warning("Please enter or select an emergency signal before processing.")