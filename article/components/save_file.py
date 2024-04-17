import os
import json
from dotenv import load_dotenv
from .parse_json import parse_json

# Load environment variables from .env file
load_dotenv()

saved_dir = os.getenv("SAVED_DIR")

def save_json_to_txt(json_data, filename):
    result = parse_json(json_data)
    
    if result is None:
        print("No valid JSON data found in save_file.py.")
    else:
        print("JSON data processed successfully.")
    print("Saving to file")
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    try:
        # Create the "saved" directory if it doesn't exist
        os.makedirs(saved_dir, exist_ok=True)
        
        # Add .txt extension to the filename if not already present
        if not filename.endswith(".txt"):
            filename += ".txt"
        
        # Construct the full path to the file
        filepath = os.path.join(saved_dir, filename)

        with open(filepath, "w", encoding="utf-8") as file:
            article_title = json_data["article_title"]
            print(article_title)
            intro = json_data["intro"]
            print(intro)
            body = ""
            for section in json_data["body"]:
                heading_title = section["heading_title"]
                heading_text = section["heading_text"]
                body += f"{heading_title}\n\n{heading_text}\n\n"
                if "subheadings" in section:
                    for subheading in section["subheadings"]:
                        subheading_title = subheading["subheading_title"]
                        subheading_text = subheading["subheading_text"]
                        body += f"{subheading_title}\n\n{subheading_text}\n\n"
            conclusion_title = json_data["conclusion_title"]
            conclusion = json_data["conclusion"]

            file.write(f"Title: {article_title}\n\n")
            file.write(f"Intro:\n{intro}\n\n")
            file.write(f"Body:\n{body}\n")
            file.write(f"Conclusion:\n{conclusion_title}\n\n{conclusion}\n")
        print(f"JSON data saved to {filepath} successfully.")
    except KeyError as e:
        print(f"Error: Missing key {e} in JSON data.")