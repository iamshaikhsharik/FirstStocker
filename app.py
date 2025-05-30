from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- Add this

app = Flask(__name__)
CORS(app)  # <--- Enable CORS for all routes

@app.route('/')
def home():
    return "Welcome to FirstStocker Bot!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'response': 'Please enter a message.'})

    # Dummy response for now
    return jsonify({'response': f'You said: {message}'})

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'image_url': ''})

    # Dummy image for now
    return jsonify({'image_url': 'https://via.placeholder.com/512?text=Coming+Soon'})

if __name__ == '__main__':
    app.run(debug=True)
