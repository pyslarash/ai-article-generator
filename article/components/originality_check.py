import requests
import json
import os
from dotenv import load_dotenv
from .turn_json_to_text import turn_json_to_text
from .parse_json import parse_json

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("ORIGINALITY_AI_KEY")
ai_probability_score = os.getenv("AI_PROBABILITY_SCORE")

def originality_check(json_data):    
    text = turn_json_to_text(json_data)
    url = "https://api.originality.ai/api/v1/scan/ai"

    payload = {
        "content": text,
        "title": "optional title",
        "aiModelVersion": "1",
        "storeScan": "false"
    }

    headers = {
        'X-OAI-API-KEY': api_key,
        'Accept': 'application/json',
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        if response_data.get("success"):
            ai_score = response_data["score"]["ai"]
            # Return True if AI score is below 0.02, False otherwise
            return float(ai_score) < float(ai_probability_score)
        else:
            error_message = response_data.get("error", "Unknown error occurred")
            return f"Error: {error_message}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Prompt user to enter text
    text_to_check = input("Please enter the text you want to check for AI usage:\n")

    # Ensure that text input is not empty
    if not text_to_check.strip():
        print("Text input is empty. Please enter some text.")
        return

    # Call the function to check AI usage
    ai_percentage = originality_check(text_to_check)

    # Display the result
    print("Did it pass:", ai_percentage)

if __name__ == "__main__":
    main()