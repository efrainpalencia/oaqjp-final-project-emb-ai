import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    json_payload = {"raw_document": {"text": text_to_analyse}}

    response = requests.post(url, headers=headers, json=json_payload)

    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()

        # Extract emotions from the response
        emotions = response_json.get("emotionPredictions", [{}])[0].get("emotion", {})

        # Find the dominant emotion
        dominant_emotion = max(emotions, key=emotions.get) if emotions else None

        # Return the formatted output
        return {
            "anger": emotions.get("anger", 0),
            "disgust": emotions.get("disgust", 0),
            "fear": emotions.get("fear", 0),
            "joy": emotions.get("joy", 0),
            "sadness": emotions.get("sadness", 0),
            "dominant_emotion": dominant_emotion
        }

    elif response.status_code == 400:
        # If status code is 400, return all values as None
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    else:
        return {
            "error": f"Request failed with status code {response.status_code}",
            "details": response.text
        }

# Example Usage
# result = emotion_detector("I hate working long hours.")
# print(json.dumps(result, indent=4))  # Pretty-print the output
