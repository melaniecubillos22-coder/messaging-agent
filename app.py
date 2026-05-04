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
	try:
		data = request.get_json()
		user_message = data.get("message", "")

		response = client.messages.create(
			model="claude-3-5-sonnet-20241022",
			max_tokens=250,
			system="""You are Shine, a warm, friendly, natural-sounding booking assistant for Maid to Shine, speak casually like a real person. Sound like a real helpful person, not a robot. Keep replies short, casual, and useful. Use a soft girly brand tone, but don’t over do emojis. Ask one helpful follow-up question at a time. If someone asks about services, explain clearly. If someone asks about products for sale, say Maid to Shine mainly provides cleaning services, but ask what type of product they’re looking for. Guide people toward booking or getting a quote.
Business info:
- Phone: (786) 475-9638
- Services: home cleaning, deep cleaning, move-in/move-out, Airbnb turnover, commercial cleaning
- Location: Miami and surrounding areas""",
			messages=[
				{"role": "user", "content": user_message}
			]
		)

		return jsonify({
			"response": response.content[0].text
		})

	except Exception as e:
		return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)