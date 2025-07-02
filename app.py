from flask import Flask, request, jsonify
import requests
import os
from utils.gpt import get_gpt_response
from utils.hubspot import create_hubspot_contact
from utils.whatsapp import send_whatsapp_message
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
print(f"[ENV] Loaded VERIFY_TOKEN: {VERIFY_TOKEN}")

# ----------------- Home Route -----------------
@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!", 200

# ----------------- GET Webhook Verification -----------------
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"[DEBUG] Mode: {mode}, Token: {token}, Challenge: {challenge}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("[✅] Webhook verified successfully.")
        return challenge, 200
    else:
        print("[❌] Webhook verification failed.")
        return "Verification failed", 403

# ----------------- POST Webhook for Incoming Messages -----------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("[📩] Incoming POST webhook:", data)

    try:
        entry = data['entry'][0]['changes'][0]['value']

        # ✅ Ignore status updates or non-message events
        if 'messages' not in entry:
            print("[ℹ️] No user message found. Ignoring this event.")
            return "No message", 200

        messages = entry['messages']
        if not messages:
            print("[ℹ️] Empty message list. Ignoring.")
            return "No content", 200

        msg = messages[0]

        if msg.get("type") != "text":
            print(f"[⚠️] Unsupported message type: {msg.get('type')}. Ignoring.")
            return "Unsupported type", 200

        phone = msg['from']
        text = msg['text']['body']
        print(f"[💬] Message from {phone}: {text}")

        # 📇 HubSpot Contact
        create_hubspot_contact(phone, text)

        # 💡 ChatGPT Response
        reply = get_gpt_response(text, phone)

        # 📤 Send Response
        send_whatsapp_message(phone, reply)

        return "OK", 200

    except Exception as e:
        print("❌ Error in /webhook:", e)
        return "Internal Server Error", 500

# ----------------- App Entry -----------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
