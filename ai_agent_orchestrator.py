from datetime import datetime
import json
import os
import time
import requests

# Optional: Uncomment if you have the openai library installed (`pip install openai requests`)
# from openai import OpenAI

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL", "https://ayu5h.app.n8n.cloud/webhook-test/0c2970a2-19f2-4125-abbc-967ecb8c08af"
)
MAKE_WEBHOOK_URL = os.getenv(
    "MAKE_WEBHOOK_URL", "https://hook.us1.make.com/your-make-webhook-id"
)

# Set to False when you plug in your real API keys and Webhook URLs
SIMULATION_MODE = True

# Simulated incoming unstructured data (e.g., fetched from an email server or form)
INCOMING_TASKS = [
    {
        "id": "TSK-101",
        "sender": "david@enterprise-client.com",
        "message": (
            "URGENT: Our production API integration is throwing 500 Internal"
            " Server Errors since your last update. Our checkout is completely"
            " down!"
        ),
    },
    {
        "id": "TSK-102",
        "sender": "sarah@startup.io",
        "message": (
            "Hi there! We love your product and are looking to upgrade to the"
            " Enterprise plan for 50 seats. Can someone from sales send over"
            " pricing?"
        ),
    },
    {
        "id": "TSK-103",
        "sender": "mike@gmail.com",
        "message": (
            "I forgot my password and the reset link isn't showing up in my"
            " inbox. Help?"
        ),
    },
]

# ==========================================
# 1. AI AGENT MODULE (OpenAI API)
# ==========================================
SYSTEM_PROMPT = """
You are an autonomous Operations Triage AI Agent. Analyze the incoming message and output ONLY a valid JSON object with the following structure:
{
    "category": "Technical_Bug" | "Sales_Lead" | "General_Support" | "Billing",
    "urgency": "High" | "Medium" | "Low",
    "sentiment": "Frustrated" | "Neutral" | "Positive",
    "summary": "1-sentence summary of the core issue",
    "draft_reply": "Polite, context-aware response ready to be sent to the user",
    "target_platform": "n8n" (if Technical_Bug or High urgency) | "Make" (for Sales_Lead, Billing, General_Support)
}
"""


def run_ai_agent(message_text):
    """Uses OpenAI API to analyze text and return structured JSON for workflow routing."""
    if SIMULATION_MODE:
        # Simulated AI Agent intelligence for local testing
        time.sleep(1)
        if "500" in message_text or "down" in message_text:
            return {
                "category": "Technical_Bug",
                "urgency": "High",
                "sentiment": "Frustrated",
                "summary": (
                    "Production API throwing 500 errors causing checkout"
                    " outage."
                ),
                "draft_reply": (
                    "Hi David, our engineering team has been alerted"
                    " immediately regarding the 500 API errors and is"
                    " investigating the outage."
                ),
                "target_platform": "n8n",
            }
        elif "Enterprise" in message_text or "pricing" in message_text:
            return {
                "category": "Sales_Lead",
                "urgency": "Medium",
                "sentiment": "Positive",
                "summary": (
                    "Customer wants to upgrade to a 50-seat Enterprise plan."
                ),
                "draft_reply": (
                    "Hi Sarah! Thrilled to hear you want to scale with us. I've"
                    " routed your request to our Enterprise Account Executive"
                    " who will email you pricing shortly."
                ),
                "target_platform": "Make",
            }
        else:
            return {
                "category": "General_Support",
                "urgency": "Low",
                "sentiment": "Neutral",
                "summary": "User is not receiving password reset emails.",
                "draft_reply": (
                    "Hi Mike, please check your spam folder. I have also"
                    " triggered a manual password reset link to your email."
                ),
                "target_platform": "Make",
            }

    # --- LIVE OPENAI API EXECUTION ---
    # client = OpenAI(api_key=OPENAI_API_KEY)
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     response_format={ "type": "json_object" },
    #     messages=[
    #         {"role": "system", "content": SYSTEM_PROMPT},
    #         {"role": "user", "content": message_text}
    #     ]
    # )
    # return json.loads(response.choices[0].message.content)


# ==========================================
# 2. MULTI-PLATFORM WEBHOOK ROUTER (REST API)
# ==========================================
def trigger_external_workflow(payload, platform):
    """Routes structured AI output to n8n or Make via REST API POST requests."""
    url = N8N_WEBHOOK_URL if platform == "n8n" else MAKE_WEBHOOK_URL

    print(
        f"   [->] Routing payload to {platform} Webhook"
        f" ({url[:35]}...)..."
    )

    if SIMULATION_MODE:
        time.sleep(0.5)
        print(
            f"   [✓] {platform} Workflow Triggered Successfully (Status: 200"
            " OK)"
        )
        return True

    # --- LIVE REST API EXECUTION ---
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        print(
            f"   [✓] {platform} Workflow Triggered! Status:"
            f" {response.status_code}"
        )
        return True
    except requests.exceptions.RequestException as e:
        print(f"   [X] Failed to trigger {platform} webhook: {e}")
        return False


# ==========================================
# 3. CONSOLE APPLICATION & EXECUTION ENGINE
# ==========================================
def main():
    print("=" * 60)
    print("🤖 AI AGENT & WORKFLOW AUTOMATION ENGINE INITIALIZED")
    print(
        f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Mode:"
        f" {'SIMULATION' if SIMULATION_MODE else 'LIVE'}"
    )
    print("=" * 60)

    for task in INCOMING_TASKS:
        print(f"\n[*] Processing Task ID: {task['id']} | From: {task['sender']}")
        print(f"   [i] Raw Input: \"{task['message'][:60]}...\"")

        # Step 1: AI Agent Analysis
        print("   [*] Engaging OpenAI Agent for intent & routing analysis...")
        ai_decision = run_ai_agent(task["message"])

        print(
            f"   [AI Output] Category: {ai_decision['category']} | Urgency:"
            f" {ai_decision['urgency']} | Sentiment: {ai_decision['sentiment']}"
        )
        print(f"   [AI Summary] {ai_decision['summary']}")

        # Step 2: Construct Unified Data Payload
        workflow_payload = {
            "task_id": task["id"],
            "sender_email": task["sender"],
            "timestamp": datetime.now().isoformat(),
            "ai_analysis": ai_decision,
        }

        # Step 3: Dynamic Multi-Platform Routing (n8n vs Make)
        target = ai_decision["target_platform"]
        trigger_external_workflow(workflow_payload, platform=target)

    print("\n" + "=" * 60)
    print("✅ ALL OPERATIONAL TASKS PROCESSED AND ROUTED SUCCESSFULLY.")
    print("=" * 60)


if __name__ == "__main__":
    main()