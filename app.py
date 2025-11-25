from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

@app.route("/sms", methods=['POST'])
def sms_reply():
    user_msg = request.values.get('Body', '').strip()
    
    headers = {"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "grok-beta",
        "messages": [{"role": "user", "content": user_msg}],
        "temperature": 0.8,
        "max_tokens": 500
    }
    
    try:
        r = requests.post(GROK_URL, json=data, headers=headers, timeout=25)
        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"]
    except:
        reply = "grok took a nap 📟 try again"

    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))