import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Set MOCK_MODE = False for live API calls
MOCK_MODE = False

# API Credentials
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Direct NVIDIA NIM API Configuration
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = "nvidia/nemotron-3.5-lightning-30b-a3b"

SYSTEM_PROMPT = """You are CrisisBridge AI, an expert real-time disaster emergency triage dispatcher.
Analyze raw emergency messages and extract structured operational intelligence.

Respond STRICTLY in valid JSON matching this schema:
{
  "disaster_type": "Flood / Earthquake / Fire / Medical / Other",
  "urgency_level": "CRITICAL / HIGH / MEDIUM / LOW",
  "location": "Extracted location or 'Unknown'",
  "victims_count": 3,
  "required_units": ["Rescue Boat", "Medical Response Team"],
  "recommended_actions": ["Immediate action 1", "Immediate action 2"],
  "summary": "1-2 sentence situation report."
}
"""

def verify_live_hazards(location: str) -> list:
    """Uses Tavily Search API to query real-time road conditions and local hazards."""
    if not TAVILY_API_KEY or "your_tavily_key" in TAVILY_API_KEY or TAVILY_API_KEY == "":
        return [
            f"Simulated live hazard report for {location}: Major waterlogging on main arterial road.",
            f"Emergency route alert: Emergency services advised to use Northern bypass."
        ]
    
    try:
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
        query = f"current disaster road closure hazard news {location}"
        response = tavily.search(query=query, search_depth="basic", max_results=3)
        return [result['content'] for result in response.get('results', [])]
    except Exception as e:
        return [
            f"Simulated hazard report for {location}: Route flooded near primary bridge access.",
            f"Emergency route alert: Use alternative high-ground access road."
        ]

def analyze_emergency_signal(user_message: str) -> dict:
    """Processes raw emergency text and fetches live web hazard verification."""
    if MOCK_MODE:
        data = {
            "disaster_type": "Flood",
            "urgency_level": "CRITICAL",
            "location": "Riverside Sector 4, Bridge Road",
            "victims_count": 3,
            "required_units": ["Rescue Boat", "Medical Response Team", "Life Jackets"],
            "recommended_actions": [
                "Dispatch flood rescue boat immediately to Sector 4",
                "Alert nearby trauma center for hypothermia treatment"
            ],
            "summary": "3 individuals trapped on a rooftop due to rapidly rising floodwaters near Sector 4."
        }
    else:
        client = OpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=NVIDIA_API_KEY
        )
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)

    # Fetch real-time web hazard intelligence using Tavily
    location = data.get("location", "")
    if location and location != "Unknown":
        data["live_hazards"] = verify_live_hazards(location)
    else:
        data["live_hazards"] = ["No specific location detected for real-time hazard verification."]

    return data

if __name__ == "__main__":
    sample_sos = "SOS! Water level reaching second floor at Riverside Sector 4."
    print("Testing Updated Triage Engine with Tavily Search...\n")
    print(json.dumps(analyze_emergency_signal(sample_sos), indent=2))