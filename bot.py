import requests
import json
import time

# ==========================
# Configuration
# ==========================

BOT_TOKEN = "8847799066:AAFAeU_Dfc0-7cXTqSsZk1l_Q-hNu5iFGyM"
EXTERNAL_API_URL = "num_live_JxQNg10MDUVbzkSh1Kwn9YkvNFBva8Hkpzqax1IK"  
DUMMY_HTTPS_SERVER = "https://example.com"

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ==========================
# Telegram API Functions
# ==========================

def get_updates(offset=None):
    url = BASE_URL + "/getUpdates"

    params = {
        "timeout": 30
    }

    if offset is not None:
        params["offset"] = offset

    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception:
        return {"ok": False, "result": []}


def send_message(chat_id, text, reply_markup=None):
    url = BASE_URL + "/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup is not None:
        data["reply_markup"] = json.dumps(reply_markup)

    try:
        requests.post(url, data=data, timeout=30)
    except Exception:
        pass


# ==========================
# Reply Keyboard
# ==========================

KEYBOARD = {
    "keyboard": [
        [
            {
                "text": "📱 Phone Lookup"
            }
        ]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}


# ==========================
# External API
# ==========================

def phone_lookup(number):
    try:
        url = EXTERNAL_API_URL + number

        response = requests.get(url, timeout=30)

        data = response.json()

        return True, json.dumps(data, indent=4)

    except Exception as e:
        return False, str(e)


# ==========================
# Message Handler
# ==========================

def handle_message(message):
    chat_id = message["chat"]["id"]

    text = message.get("text", "").strip()

    if text == "/start":
        send_message(
            chat_id,
            "👋 Welcome!\n\nChoose an option below.",
            KEYBOARD
        )
        return

    if text == "📱 Phone Lookup":
        send_message(
            chat_id,
            "📞 Send 10 digit mobile number:"
        )
        return

    if text.isdigit() and len(text) == 10:

        success, result = phone_lookup(text)

        if success:
            send_message(
                chat_id,
                "<pre>{}</pre>".format(result)
            )
        else:
            send_message(
                chat_id,
                "❌ API Error:\n<pre>{}</pre>".format(result)
            )

        return

    send_message(
        chat_id,
        "❌ Invalid input.\n\nPlease send a valid 10 digit mobile number."
    )


# ==========================
# Main Polling Loop
# ==========================

def main():
    offset = None

    while True:
        updates = get_updates(offset)

        if updates.get("ok"):

            for update in updates["result"]:

                offset = update["update_id"] + 1

                if "message" in update:
                    handle_message(update["message"])

        time.sleep(1)


if __name__ == "__main__":
    main()
