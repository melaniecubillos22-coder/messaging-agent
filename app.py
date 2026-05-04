from flask import Flask, request, jsonify
import os
from anthropic import Anthropic

app = Flask(__name__)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return "Messaging Agent is running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=250,
        system="You are a friendly, girly, professional customer service agent for Maid to Shine, a maid cleaning service. Respond warmly, keep messages short, ask what service they need, their location, preferred date/time, home size, and contact info. Help customers book cleaning appointments. Do not mention you are AI.",
        messages=[{"role": "user", "content": user_message}]
    )

    return jsonify({
        "response": response.content[0].text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)