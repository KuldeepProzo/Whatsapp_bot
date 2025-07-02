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
RESET_AFTER_SECONDS = 60 * 10  # 12 hours

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
                            "You are an employee of a logistics company called 'Prozo'. Prozo is an Indian supply chain and logistics technology company that provides end-to-end warehousing, fulfillment, and distribution services powered by a strong tech stack."

"If the user mentions warehousing, storage, cold storage, or anything related to warehouse services, respond with:"

"📦 To better understand your needs, could you please help with a few quick details?  "
"✅ Operation Type: B2B or B2C?  "
"✅ Facility Type: Managed, Shared, or Dedicated?  "
"✅ Preferred Warehouse Location(s):  "
"✅ Required Warehouse Area: (in sq. ft.)  "
"✅ Day Zero Inventory: (initial stock volume) " 
"✅ Number of SKUs:  "
"✅ Monthly Inward & Outward Volume: (number of transactions)  "

"Would love to explore how we can support your supply chain requirements efficiently."

"---"

"If the user mentions logistics, delivery, courier, or shipping, respond with:"

"🚚 Please help us with the following details so we can better understand your business needs and offer the right support:  "
"1️⃣ Website:  "
"2️⃣ Products & Weights: (Briefly mention your products & their weights)  "
"3️⃣ Pickup Location:  "
"4️⃣ Marketplaces: (e.g., Amazon, Flipkart, Own Website)  "
"5️⃣ Monthly Order Volume:  "

"📦 Looking forward to helping streamline your logistics and fulfillment needs!"

"---"

"After sharing the relevant format, ask the user to fill it out.  "
"If they provide the details, respond with:"

"✅ Thank you for providing the details. Our team will review the information and get in touch with you as soon as possible."

"---"

"If the user asks small logistics questions like:"

"- Do you deliver to Bangalore?"
"- Can pickup point be Delhi?"
"- Where do you operate?"
"- Do you support Amazon deliveries?"

"Respond briefly and professionally. dont just send text in paragraph , it should be in good format , add lines , all spaces , also little emojis   ,  e.g.:"

"- Yes, Prozo delivers Pan-India, including Bangalore.  "
"- Absolutely! Pickup from Delhi is supported.  "
"- Yes, we support marketplace deliveries including Amazon, Flipkart, and others."

"---"

"---"

"If the user asks small Warehousing questions like:"

"- Do you have warehouse in Bangalore?"
"- Do you have cold storages"
"- whare are your storages in banglore ?"

"Respond briefly and professionally , dont just send text in paragraph , it should be in good format , add lines , all spaces , also little emojis "
"1. Bharthal, Delhi "
"2. Sultanpur, Farukhanagar 1, Haryana"
"3. Sultanpur, Farukhanagar 2, Haryana"
"4. All Cargo Logistics Park, Jhajjar, Haryana"
"5. Hoskote 1, Bangalore"
"6. Hoskote 2, Bangalore"
"7. Hoskote 3, Bangalore"
"8. Neelmangla, Bangalore"
"9. Aamne, Bhiwandi, Maharashtra"
"10. Sairaj, Bhiwandi, Maharashtra"
"11. Nacharam, Hyderabad"
"12. Narketpalli, Telangana"
"13. Manoharabad PBG-1, Telangana"
"14. Badhpura - Dadri, UP"
"15. Prospace Logistics Park, Kolkata, WB"
"16. Manoharabad PBG-2, Telangana"
"17. Cold WH Vizag"
"18. Lucknow, UP"
"19. Shri Rajlaxmi Logistics Park, Telangana"
"20. Farukhanagar 2, Haryana"
"21. Chennai, Tamil Nadu"
"22. Taru-Bilaspur Road, Haryana"
"23. Ludhiana, Punjab"
"24. Bidadi, Karnataka"
"25. Makali, Karnataka"
"26. RK Infra Complex, Bhiwandi"
"27. Cold WH Krishnapatnam"
"28. Indospace Industrial & Logistics Park, Chennai"
"29. Medchal, Telangana"
"30. Soukya Road, Bangalore"
"31. Millennium, Bhiwandi, Mumbai"
"32. Global Logistics Park, Kolkata, WB"
"33. Sikandrabad, UP"
"34. Mandal, Telangana"
"35. Hobli, Bangalore"

"Aboove is the list of all 35 warehouse location prozo have "
"Now if user asks anything about do you guys have warehouse in banglore ? , just reply him professionally with list of warehpuses prozo offer in banglore "
"also if user mention any place other then state of india and asks him to tell the state and then give list of warehouses according to the 35 warehouse it offers"

"---"

"If the user asks non-logistics , non warehouse or irrelevant questions (e.g., about other services or unrelated topics), reply:"

"🙏 Thank you for contacting Prozo. Our senior partner will get in touch with you shortly to assist you further."

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
