import json
from .parse_json import parse_json

def turn_json_to_text(json_data):
    # First, attempt to parse the input using your custom parsing function
    result = parse_json(json_data)
    
    if result is None:
        print("No valid JSON data found.")
        return ""  # Exit early if the result is None
    else:
        print("JSON data processed successfully.")

    print("Generating text content")
    
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError:
            print("Failed to decode JSON.")
            return False
    print("JSON data processed successfully after decoding.")

    try:
        # Extract data from JSON
        article_title = json_data["article_title"]
        intro = json_data["intro"]
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

        text_content = f"Title: {article_title}\n\n"
        text_content += f"Intro:\n{intro}\n\n"
        text_content += f"Body:\n{body}\n"
        text_content += f"Conclusion:\n{conclusion_title}\n\n{conclusion}\n"
        print("Text content generated successfully.")
        return text_content
    except KeyError as e:
        print(f"Error: Missing key {e} in JSON data.")
        return ""