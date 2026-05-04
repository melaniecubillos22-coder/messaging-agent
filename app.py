import anthropic
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()
    user_message = data.get('message', '')

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=20000,
        system="maid cleaning service, nice, girly, friendly but business oriented short responses",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_message
                    }
                ]
            }
        ],
        thinking={
            "type": "adaptive"
        }
    )
    response = message.content[0].text if message.content else ""
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)