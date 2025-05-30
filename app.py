from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to FirstStocker Bot!'

# Existing routes
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    # Implement Groq API call here
    response = {"response": "This is a placeholder response."}
    return jsonify(response)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    prompt = request.json.get('prompt')
    # Implement Hugging Face API call here
    image_url = "https://via.placeholder.com/150"
    return jsonify({"image_url": image_url})
