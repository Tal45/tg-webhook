from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE")
ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID"))
DEBUGGING_JSON = True if os.getenv("DEBUGGING_JSON").lower() == "true" else False
@app.route('/', methods=['GET'])
def home():
    return 'Server is running!', 200

@app.route('/webhook', methods=['POST'])
def telegram_webhook():

    # get and validate msg
    data = request.json
    if DEBUGGING_JSON:
        print("Incoming webhook:", data, flush=True)

    # Accept both normal messages and channel posts
    message = data.get('message') or data.get('channel_post')

    if not message:
        print("No message or channel_post found. Ignoring.", flush=True)
        return 'ok', 200  # Soft ignore system events like my_chat_member

    message = data.get('message') or data.get('channel_post')
    text = message.get('text')
    chat = message.get('chat', {})
    chat_id = chat.get('id')

    if chat_id != ALLOWED_CHAT_ID:
        return 'Unauthorized - wrong chat', 401

    if not text:
        return 'No text to process', 200  # ignore non-text msgs (stickers etc.)

    print(f"Received valid message: {text}",  flush=True)

    # save to supabase
    save_message_to_supabase(text)

    return 'ok', 200


def save_message_to_supabase(text):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "fetched": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print("Message saved to Supabase.",  flush=True)
        else:
            print(f"Error saving message: {response.text}", flush=True)
    except Exception as e:
        print(f"Exception while saving to Supabase: {e}",  flush=True)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
