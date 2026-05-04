from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from anthropic import Anthropic

app = Flask(__name__)
CORS(app)

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
system="You are a friendly, girly, professional customer service agent for Maid to Shine, a maid cleaning service. Be warm, helpful, and guide customers to book.",
messages=[
{"role": "user", "content": user_message}
]
)

return jsonify({
"response": response.content[0].text
})

if __name__ == "__main__":
app.run(host="0.0.0.0", port=5000)