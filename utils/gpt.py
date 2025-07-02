import os
import time
import traceback
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chat history store
user_histories = {}

# First prompt message for new or reset user
first_prompt = (
    
    "👋 Hi, this is Piyush from Prozo!\n "
    "We help brands like yours with end-to-end fulfillment & supply chain solutions across India.\n"
    "✨ Could you please share what you're currently looking for?\n"
    "  🧱 1. Warehouse Space  \n"
    "  📦 2. Warehouse Management Services (WMS)\n"  
    "  🚚 3. Logistics & Transportation Services\n"  
    "  🧰 4. All of the Above\n "  

    "Looking forward to understanding your needs and assisting you better! 🚀\n"

        )

# Reset user chat if inactive for more than 12 hours
RESET_AFTER_SECONDS = 12 * 60 * 60  # 12 hours

# Default fallback response
fallback_response = (
    "Thank you for contacting Prozo. Our senior`s will get in touch with you shortly to assist you further. 🙏"
)

def get_gpt_response(message, user_id):
    """
    Handles user message and generates GPT response with memory.

    Args:
        message (str): Incoming WhatsApp message
        user_id (str): User phone number or ID

    Returns:
        str: Assistant reply
    """
    try:
        now = time.time()
        is_new = False

        # Check if new user or session expired
        if (user_id not in user_histories or 
            now - user_histories[user_id]["last_ts"] > RESET_AFTER_SECONDS):
            
            user_histories[user_id] = {
                "history": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant for a logistics company called 'Prozo'. "
                            "If user says anything about wharehousing just send him the following message in a correctFormat , To better understand your needs, could you please help with a few quick details? 👇✅ Operation Type: B2B or B2C?✅ Facility Type: Managed, Shared, or Dedicated?✅ Preferred Warehouse Location(s):✅ Required Warehouse Area: (in sq. ft.)✅ Day Zero Inventory: (initial stock volume)✅ Number of SKUs:✅ Monthly Inward & Outward Volume: (number of transactions)Would love to explore how we can support your supply chain requirements efficiently."
                            "If user says anything about Logistics just send him the following message in a correctFormat , ✨ Please help us with the following details so we can better understand your business needs and offer the right support:1️⃣ Website:2️⃣ Products & Weights: (Briefly mention your products & their weights)3️⃣ Pickup Location: (Your Pickup Location)4️⃣ Marketplaces: We are currently selling on Amazon / Flipkart / Own Website5️⃣ Monthly Order Volume: (Your Monthly Order Volume)📦 Looking forward to helping streamline your logistics and fulfillment needs! 🚛"


                            "Answer user queries about delivery times, locations, shipping cost, company details, etc. "
                            "Be short and professional. If the user goes off-topic or asks non-logistics questions, say: "
                            "'Thank you for contacting Prozo. Our senior partner will get in touch with you shortly to assist you further. 🙏'"
                        )
                    },
                    {
                        "role": "assistant",
                        "content": first_prompt
                    }
                ],
                "last_ts": now
            }
            is_new = True

        if is_new:
            return first_prompt

        # Append user message
        user_histories[user_id]["history"].append({"role": "user", "content": message.strip()})
        user_histories[user_id]["last_ts"] = now

        # GPT API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=user_histories[user_id]["history"]
        )

        reply = response.choices[0].message.content.strip()

        # Append assistant message
        user_histories[user_id]["history"].append({"role": "assistant", "content": reply})

        return reply

    except Exception as e:
        print("❌ GPT Error:", e)
        traceback.print_exc()
        return fallback_response
