from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
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
        prompt = data.get('prompt')  
        if prompt is None:
            return jsonify({"error": "No prompt received"}), 400

        print(f"Received prompt: {prompt}")

        ai_response = ai_function(prompt)
        
        ai_response = (ai_function(prompt).head(30)).astype(str)
        filtered_response = ai_response[["Track Name", "Artist Name(s)"]]
        to_return = filtered_response.to_dict(orient="records")
        return jsonify(to_return)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)


    