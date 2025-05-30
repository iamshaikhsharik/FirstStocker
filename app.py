from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

# API credentials
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"
HF_IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HF_TOKEN = "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"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')

        # If user asks for an image
        if any(word in user_input.lower() for word in ["draw", "generate image", "create image"]):
            image_payload = {"inputs": user_input}
            image_headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            image_response = requests.post(HF_IMAGE_API_URL, headers=image_headers, json=image_payload)

            if image_response.status_code == 200 and image_response.headers.get("Content-Type", "").startswith("image"):
                # Encode image to base64
                encoded_image = base64.b64encode(image_response.content).decode('utf-8')
                image_data_url = f"data:image/png;base64,{encoded_image}"
                return jsonify({"reply": "Here's the image you requested:", "image": image_data_url})
            else:
                return jsonify({"reply": "Failed to generate image."})

        # Otherwise, send to Groq chat model
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are FirstStocker, a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
        else:
            reply = "Failed to connect to Groq API."

        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'reply': f"Internal error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
