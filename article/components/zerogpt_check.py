import requests
import os
from dotenv import load_dotenv
from .turn_json_to_text import turn_json_to_text
import json
from .parse_json import parse_json

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("ZEROGPT_KEY")
ai_probability_score = os.getenv("AI_PROBABILITY_SCORE")

def zerogpt_check(json_data):    
    text = turn_json_to_text(json_data)
    # ZeroGPT API endpoint for detecting AI-generated text
    endpoint = "https://api.zerogpt.com/api/detect/detectText"

    # Set headers with API key
    headers = {
        "Content-Type": "application/json",
        "ApiKey": api_key
    }

    # Data to be sent in the request
    data = {
        "input_text": text
    }

    try:
        # Send POST request to ZeroGPT API
        response = requests.post(endpoint, headers=headers, json=data)
        response_data = response.json()

        # Check if request was successful
        if response_data["success"]:
            # Return fakePercentage if available
            fake_percentage = response_data["data"].get("fakePercentage")
            if fake_percentage is not None:
                # Convert fakePercentage to a value between 0 and 1
                fake_percentage_normalized = fake_percentage / 100.0
                # Return True if below 0.02, False otherwise
                return float(fake_percentage_normalized) < float(ai_probability_score)
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
def main():
    # Prompt user to input text
    text_to_check = input("Please enter the text you want to check for AI-generated content:\n")

    # Call the function to check AI-generated content
    result = zerogpt_check(text_to_check)

    # Display the result
    print("AI Check Result:")
    if isinstance(result, str):
        print(result)
    else:
        print(f"Did it pass: {result}")

if __name__ == "__main__":
    main()