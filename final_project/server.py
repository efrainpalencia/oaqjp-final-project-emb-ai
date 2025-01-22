"""
Flask application for emotion detection.
Handles API requests and returns formatted emotion analysis responses.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def home():
    """
    Serves the home page.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def detect_emotion():
    """
    Handles emotion detection API calls.
    Expects a JSON request with a 'text' field.
    Returns emotion analysis results or an error message.
    """
    response = {}
    status_code = 200  # Default to success

    try:
        # Get JSON data from the request
        data = request.get_json()
        if not data or "text" not in data:
            response = {"error": "Invalid input. Please provide a text field."}
            status_code = 400
        else:
            text = data["text"]
            result = emotion_detector(text)

            if result["dominant_emotion"] is None:
                response = {"response": "Invalid text! Please try again!"}
                status_code = 400
            else:
                response_text = (
                    f"For the given statement, the system response is 'anger': {result['anger']}, "
                    f"'disgust': {result['disgust']}, 'fear': {result['fear']},  "
                    f"'joy': {result['joy']}, "
                    f"'sadness': {result['sadness']}. "
                    f"The dominant emotion is {result['dominant_emotion']}."
                )
                response = {"response": response_text}

    except KeyError:
        response = {"error": "Invalid JSON structure. 'text' field is required."}
        status_code = 400
    except TypeError:
        response = {"error": "Invalid input type. Please provide a valid JSON request."}
        status_code = 400
    except ValueError:
        response = {"error": "Unexpected value error occurred. Please check your input."}
        status_code = 400
    except (ConnectionError, TimeoutError):
        response = {"error": "Network issue. Please try again later."}
        status_code = 503
    except RuntimeError:
        response = {"error": "A runtime error occurred. Please try again later."}
        status_code = 500

    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
