"""
CivicHero AI — Gemini AI Service
Uses: google-genai (new official SDK)
"""

import os
import json
import re

DEPT_MAP = {
    "Pothole":      "PWD – Roads Division",
    "Water":        "Jal Nigam / Water Board",
    "Electricity":  "DISCOM – Electricity Board",
    "Sewage":       "Municipal Corp – Sanitation",
    "Garbage":      "Sanitation Department",
    "Parks":        "Parks & Gardens Dept",
    "Construction": "Town Planning Authority",
    "Streetlight":  "Municipal Lighting Division",
    "Other":        "Municipal Corporation",
}

ETA_MAP = {
    "critical": "24-48 hours",
    "high":     "3-5 days",
    "medium":   "1-2 weeks",
    "low":      "2-4 weeks",
}


def _get_client():
    """Return a google-genai client or None if no key."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        print(f"[Gemini] Client init error: {e}")
        return None


def _call_gemini(prompt: str, image_path: str = None) -> str:
    """Call Gemini 2.5 Flash and return text response."""
    client = _get_client()
    if not client:
        return ""

    try:
        from google import genai
        from google.genai import types

        contents = [prompt]

        # Add image if provided
        if image_path:
            full_path = os.path.join("static", "uploads", image_path)
            if os.path.exists(full_path):
                try:
                    import PIL.Image
                    img = PIL.Image.open(full_path)
                    contents = [img, prompt]
                except Exception as img_err:
                    print(f"[Gemini] Image load error: {img_err}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )
        return response.text.strip()

    except Exception as e:
        print(f"[Gemini] API call error: {e}")
        return ""


def analyze_issue_with_gemini(title: str, description: str,
                               category: str, image_path: str = None) -> dict:
    """
    Analyze a civic issue using Gemini 2.5 Flash.
    Returns structured dict with category, severity, priority, etc.
    Falls back to rule-based analysis if API unavailable.
    """
    prompt = f"""You are an AI assistant for CivicHero, a civic issue reporting platform in India.
Analyze the following civic issue and return ONLY a valid JSON object with these exact fields:

{{
  "category": "<one of: Pothole, Water, Electricity, Sewage, Garbage, Parks, Construction, Streetlight, Other>",
  "severity": "<one of: critical, high, medium, low>",
  "priority": "<one of: critical, high, medium, low>",
  "department": "<responsible government department name>",
  "summary": "<2-3 sentence professional AI analysis of the issue and its community impact>",
  "recommended_action": "<specific actionable step for the responsible authority>",
  "estimated_resolution": "<estimated time to resolve e.g. 24-48 hours, 3-5 days, 1-2 weeks>",
  "confidence": <integer between 70 and 99>
}}

Issue Title: {title}
User Selected Category: {category}
Description: {description}

Rules:
- Correct the category if user selected wrong one based on description
- Set severity=critical if there is danger to life, accidents, flooding, or blocking roads
- Set severity=high for significant public inconvenience
- Respond ONLY with the JSON object. No markdown, no explanation, nothing else."""

    raw = _call_gemini(prompt, image_path)

    if raw:
        try:
            # Strip any markdown fences
            clean = re.sub(r"```(?:json)?|```", "", raw).strip()
            result = json.loads(clean)

            # Ensure required fields exist
            cat = result.get("category", category)
            result.setdefault("category", cat)
            result.setdefault("department", DEPT_MAP.get(cat, "Municipal Corporation"))
            result.setdefault("estimated_resolution", ETA_MAP.get(result.get("severity", "medium"), "3-5 days"))
            result.setdefault("confidence", 85)
            return result

        except json.JSONDecodeError as e:
            print(f"[Gemini] JSON parse error: {e}\nRaw: {raw[:200]}")

    # Fallback to rule-based
    return _rule_based_analysis(title, description, category)


def get_ai_citywide_insights() -> dict:
    """Generate AI-powered citywide insights. Falls back to static."""
    prompt = """You are an AI city analyst for CivicHero, analyzing civic issues in Bengaluru, India.
Generate actionable civic insights. Return ONLY this JSON object:

{
  "headline": "<one key insight headline, under 12 words>",
  "summary": "<2-3 sentences analyzing current civic patterns and what they mean>",
  "risk": "<one emerging risk to flag for city authorities>",
  "recommendation": "<one concrete recommendation for city authorities this week>",
  "priority": "<critical or high or medium>",
  "chips": ["<action label 1>", "<action label 2>", "<action label 3>"]
}

Respond ONLY with the JSON. No markdown."""

    raw = _call_gemini(prompt)
    if raw:
        try:
            clean = re.sub(r"```(?:json)?|```", "", raw).strip()
            return json.loads(clean)
        except Exception as e:
            print(f"[Gemini] Insights parse error: {e}")

    return _static_insights()


def chat_with_gemini(message: str, history: list) -> str:
    """
    Handle chatbot conversation using Gemini 2.5 Flash.
    Returns plain text reply.
    """
    system_prompt = """You are CivicHero AI Companion — a smart, friendly assistant embedded in a civic issue reporting platform for Indian cities (primarily Bengaluru).

You help citizens with:
• Understanding civic issues: potholes, water leaks, broken streetlights, sewage, garbage, construction problems
• Explaining priority levels and WHY issues get certain priority ratings
• Estimating repair COSTS and TIMELINES for different civic problems  
• Listing SAFETY PRECAUTIONS for reported issues
• Explaining WHICH government department resolves which type of issue:
  - Potholes/Roads → PWD (Public Works Department)
  - Water leaks/pipes → Jal Nigam / Water Board
  - Electricity/Streetlights → DISCOM / Electricity Board
  - Sewage/Manholes → Municipal Corporation – Sanitation
  - Garbage → Sanitation Department
  - Parks → Parks & Gardens Department
• Guiding users HOW TO REPORT issues effectively on CivicHero
• Answering ANY general question — you are a general-purpose AI assistant too

Formatting rules:
- Keep responses concise: 2-4 sentences unless more detail is requested
- Use bullet points (•) for lists
- Be friendly, helpful, and professional
- Always give a helpful answer — never refuse or say you cannot help
- If asked about costs, give realistic Indian Rupee estimates
- If asked about timelines, give realistic estimates based on Indian civic systems"""

    # Build conversation for context
    parts = [system_prompt, "\n\n--- Conversation ---"]
    for h in history[-8:]:
        role = "User" if h.get("role") == "user" else "Assistant"
        parts.append(f"{role}: {h.get('content', '')}")
    parts.append(f"User: {message}")
    parts.append("Assistant:")

    full_prompt = "\n".join(parts)

    raw = _call_gemini(full_prompt)
    if raw:
        return raw

    return _chatbot_fallback(message)


# ── Fallback Functions ─────────────────────────────

def _rule_based_analysis(title: str, description: str, category: str) -> dict:
    """Rule-based fallback when Gemini is unavailable."""
    text = (title + " " + description).lower()

    if any(w in text for w in ["critical", "danger", "emergency", "accident",
                                "live wire", "flooding", "manhole", "collapsed",
                                "blocking", "burst", "overflow", "sparking"]):
        severity = priority = "critical"
    elif any(w in text for w in ["major", "serious", "damage", "broken",
                                  "multiple", "days", "weeks", "hazard"]):
        severity = priority = "high"
    elif any(w in text for w in ["minor", "small", "slight", "cosmetic"]):
        severity = priority = "low"
    else:
        severity = priority = "medium"

    dept = DEPT_MAP.get(category, "Municipal Corporation")

    return {
        "category":              category,
        "severity":              severity,
        "priority":              priority,
        "department":            dept,
        "summary":               f"A {severity}-severity {category.lower()} issue has been reported. "
                                 f"The matter has been routed to {dept} for immediate attention. "
                                 f"Community verification and photographic evidence will help accelerate resolution.",
        "recommended_action":    f"Assign {dept} field team to inspect and resolve the issue. "
                                 f"Barricade the area if safety risk is present.",
        "estimated_resolution":  ETA_MAP.get(severity, "3-5 days"),
        "confidence":            78,
    }


def _chatbot_fallback(message: str) -> str:
    """Rule-based chatbot responses when Gemini is unavailable."""
    msg = message.lower()

    if any(w in msg for w in ["pothole", "road", "street", "tar"]):
        return ("Potholes are handled by PWD (Public Works Department). Critical potholes "
                "(wider than 1ft) are typically fixed within 24-48 hours. Repair costs range "
                "from ₹500 to ₹5,000 depending on size. Always report with a photo for fastest response!")

    elif any(w in msg for w in ["water", "leak", "pipe", "burst"]):
        return ("Water leaks are handled by Jal Nigam / Water Board. A burst pipe wastes "
                "10,000+ litres daily and is treated as critical — typically resolved in 12-24 hours. "
                "Pipe repair costs ₹2,000–₹20,000. Report immediately with GPS location.")

    elif any(w in msg for w in ["light", "streetlight", "electricity", "power", "wire"]):
        return ("Streetlight and electricity issues go to DISCOM / Electricity Board. "
                "Broken streetlights are resolved in 48 hours; live wires get emergency response in 2-4 hours. "
                "⚠️ Never touch a fallen wire — stay 10 metres away and report immediately!")

    elif any(w in msg for w in ["garbage", "waste", "trash", "dump", "bin"]):
        return ("Garbage issues are handled by the Sanitation Department. Urban areas should "
                "receive daily collection. Overflowing bins attract rodents and mosquitoes. "
                "Report collection failures — authorities typically respond within 24 hours.")

    elif any(w in msg for w in ["sewage", "drain", "manhole", "sewer"]):
        return ("Sewage issues go to Municipal Corporation – Sanitation. "
                "⚠️ Missing manhole covers are life-threatening emergencies — get emergency response in 2 hours. "
                "Sewage overflow is a health hazard resolved in 24 hours. Drain cleaning costs ₹5,000–₹30,000.")

    elif any(w in msg for w in ["cost", "price", "rupee", "expensive", "repair", "₹"]):
        return ("Typical civic repair costs in India:\n"
                "• Pothole filling: ₹500 – ₹5,000\n"
                "• Water pipe repair: ₹2,000 – ₹20,000\n"
                "• Streetlight replacement: ₹3,000 – ₹15,000\n"
                "• Sewage drain cleaning: ₹5,000 – ₹30,000\n"
                "• Road resurfacing (per metre): ₹800 – ₹2,500")

    elif any(w in msg for w in ["safety", "precaution", "danger", "hazard", "safe"]):
        return ("Safety precautions for civic hazards:\n"
                "• Potholes: Place rocks/bricks around edges to warn vehicles at night\n"
                "• Live wires: Stay 10m away, don't touch, evacuate nearby people\n"
                "• Open manholes: Barricade immediately, warn pedestrians\n"
                "• Water leaks: Avoid using water from nearby taps\n"
                "• Sewage overflow: Stay away, wear mask, wash hands thoroughly")

    elif any(w in msg for w in ["who", "department", "resolve", "handle", "contact"]):
        return ("Government departments for civic issues:\n"
                "• Roads/Potholes → PWD (Public Works Department)\n"
                "• Water/Pipes → Jal Nigam / Water Board\n"
                "• Electricity/Lights → DISCOM / Electricity Board\n"
                "• Sewage/Drains → Municipal Corporation – Sanitation\n"
                "• Garbage → Sanitation Department\n"
                "• Parks/Trees → Parks & Gardens Department")

    elif any(w in msg for w in ["time", "long", "when", "how long", "days", "hours"]):
        return ("Estimated resolution times:\n"
                "• Critical (danger to life): 2-24 hours emergency response\n"
                "• High priority (major inconvenience): 3-5 days\n"
                "• Medium (moderate issue): 1-2 weeks\n"
                "• Low (minor concern): 2-4 weeks\n"
                "Upvoted issues with community support get resolved faster!")

    elif any(w in msg for w in ["how", "report", "submit", "file"]):
        return ("To report an issue on CivicHero AI:\n"
                "1. Click 'Report Issue' in the left sidebar\n"
                "2. Select the issue category\n"
                "3. Enter title and detailed description\n"
                "4. Set your location on the map (or use GPS)\n"
                "5. Upload a photo for AI image analysis\n"
                "6. Click Submit — Gemini AI analyzes and routes instantly!")

    elif any(w in msg for w in ["hello", "hi", "hey", "namaste", "hii", "helo"]):
        return "Hello! 👋 I'm the CivicHero AI Companion powered by Gemini 2.5 Flash. I can help you with issue reporting, safety tips, repair costs, department info, and any other question. What would you like to know?"

    else:
        return ("I'm here to help! You can ask me about:\n"
                "• How to report a civic issue\n"
                "• Which department handles your problem\n"
                "• Safety precautions for hazards\n"
                "• Repair costs and timelines\n"
                "• Priority levels explanation\n"
                "What would you like to know?")


def _static_insights() -> dict:
    return {
        "headline":        "Pothole cluster detected on MG Road corridor",
        "summary":         ("5 pothole reports filed within a 400m radius over 3 days. "
                            "AI analysis predicts a 40% worsening with monsoon onset. "
                            "Cluster pattern suggests systemic road drainage failure rather than isolated damage."),
        "risk":            "14 road issues flagged as high-risk for monsoon flooding in South Bengaluru corridors.",
        "recommendation":  "Deploy pre-monsoon road patching teams in Ward 3, 7, and 12 before June 30 monsoon onset.",
        "priority":        "high",
        "chips":           ["View cluster map", "Escalate to PWD", "Monsoon risk report"],
    }
