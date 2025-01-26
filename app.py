from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.AI_Integration import ai_function

app = Flask(__name__, template_folder='frontend', static_folder="frontend")
CORS(app, origins=["http://127.0.0.1:5500"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-prompt', methods=['POST'])
def process_prompt():
    try:
        data = request.get_json()
        print("Received request data:", data)  
        prompt = data.get('prompt')  # Extract the 'prompt' key
        if prompt is None:
            return jsonify({"error": "No prompt received"}), 400

        print(f"Received prompt: {prompt}")

        # Pass the prompt to your AI processing function
        ai_response = ai_function(prompt)
        # Cut it to 30 songs
        ai_array = ai_response[:30]
          
        print("Playlist: " + ai_array)

        # Return the AI response as a JSON response
        response = {
            "message": ai_array,
            "status": "success"
        }


        return jsonify(response)  # Send a JSON response back to the frontend
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)