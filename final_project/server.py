from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def detect_emotion():
    try:
        # Get JSON data from the request
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Invalid input. Please provide a text field."}), 400
        
        text = data["text"]
        result = emotion_detector(text)

        # Check if the dominant emotion is None (invalid input case)
        if result["dominant_emotion"] is None:
            return jsonify({"response": "Invalid text! Please try again!"}), 400

        # Format the response as requested
        response_text = (
            f"For the given statement, the system response is 'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, 'fear': {result['fear']}, 'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
        )

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
