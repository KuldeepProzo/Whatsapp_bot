import requests
import os

def create_hubspot_contact(phone, message):
    HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")
    headers = {
        "Authorization": f"Bearer {HUBSPOT_TOKEN}",
        "Content-Type": "application/json"
    }

    # Step 1: Check if contact already exists
    search_url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
    search_payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "phone",
                        "operator": "EQ",
                        "value": phone
                    }
                ]
            }
        ],
        "properties": ["phone"]
    }

    search_response = requests.post(search_url, headers=headers, json=search_payload)
    search_result = search_response.json()

    if search_response.status_code == 200 and search_result.get("total", 0) > 0:
        print(f"HubSpot: Number {phone} already in contacts ✅")
        return  # Do not proceed to create contact

    # Step 2: Create new contact if not found
    data = {
        "properties": {
            "phone": phone,
            "firstname": "WhatsApp Lead",
            "lastname": phone[-4:],  # Last 4 digits as dummy name
            "company": "Prozo",
            "message": message
        }
    }

    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/contacts",
        headers=headers,
        json=data
    )

    print("HubSpot response:", response.status_code, response.text)
