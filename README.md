# 🚨 CrisisBridge AI — Real-Time Disaster Triage & Emergency Logistics Agent

> **Built for the Nebius × NVIDIA Global AI Hackathon**

CrisisBridge AI is an intelligent disaster emergency response platform designed to automate incoming SOS triage, assess medical urgency, determine unit dispatch needs, and verify live road/hazard conditions during natural disasters.

---

## 💡 Key Features

- **Automated Distress Signal Triage**: Processes raw, unstructured SOS text (messages, social feeds, transcriptions) into structured operational intelligence.
- **Urgency & Resource Assessment**: Extracts disaster category, victim count, urgency tier (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), and recommended rescue equipment.
- **Live Hazard Route Verification**: Integrates **Tavily Search API** to fetch real-time local web news and road closures around disaster sites to prevent dispatching units into blocked routes.
- **Interactive Dispatcher Dashboard**: Clean Streamlit dashboard for real-time emergency monitoring.

---

## 🛠️ Technology Stack & AI Models

- **LLM Reasoning**: NVIDIA Nemotron-4 (`nvidia/nemotron-4-340b-instruct`) served via **Nebius Token Factory** & **Nebius AI Cloud**.
- **Real-Time Web Search**: **Tavily Search API** for live web hazard verification.
- **Frontend Dashboard**: Streamlit (Python).
- **API Architecture**: OpenAI Python SDK compatible client.

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/crisisbridge-ai.git](https://github.com/your-username/crisisbridge-ai.git)
cd crisisbridge-ai