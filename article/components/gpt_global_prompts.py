import os
import requests
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()
gpt_engine = os.getenv("MAIN_CHAT_GPT_ENGINE")
stability_key = os.getenv("STABILITY_API_KEY")
img_dir = os.getenv("IMG_DIR")
pitch_dir = os.getenv("PITCH_DIR")
temp = float(os.getenv("TEMPERATURE"))
freq_pen = float(os.getenv("FREQUENCY_PENALTY"))
pres_pen = float(os.getenv("PRESENCE_PENALTY"))

rules_file="rules.txt"
with open(rules_file, 'r') as file:
    rules = file.read()

def write_pitch(summary):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are a professional guest blog writer who successfully pitches articles to other blogs or websites."},
            {"role": "user", "content": f"You just wrote an article that you have to pitch to another blog. "
                                        f"Make sure that your pitch cannot be detected by any AI detectors. Use a friendly and persuasive tone making the blog to publish your article. "
                                        f"Utilize various ways to bypass the AI-check detectors. Only return your pitch and nothing else. "
                                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                                        f"This is the summary of an article that you are pitching: {summary}"}
        ]
    )
    pitch_text = response.choices[0].message.content
    return pitch_text

def save_pitch_to_file(summary, filename):
    # Ensure the pitch directory exists
    os.makedirs(pitch_dir, exist_ok=True)
    
    # Generate the pitch text
    pitch_text = write_pitch(summary)
    
    # Determine the full file path
    file_path = os.path.join(pitch_dir, f"{filename}.txt")
    
    # Save the pitch text to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pitch_text)
    
    print(f"Pitch saved successfully to {file_path}")

def cover_image_prompt_generator(summary):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a professional Stability AI image generation prompt writer."},
            {"role": "user", "content": f"Create a prompt for a cover image based on a summary of this article: {summary}"}
        ]
    )
    
    return response.choices[0].message.content

def cover_image_generator(summary, num_img, filename):
    # Ensure the image directory exists
    os.makedirs(img_dir, exist_ok=True)
    
    # Loop to generate each image with a unique prompt
    for index in range(num_img):
        prompt = cover_image_prompt_generator(summary)  # Generate a new prompt for each image

        # Initialize headers and data payload for the API request
        headers = {
            "authorization": f"Bearer {stability_key}",
            "accept": "application/json"
        }
        data = {
            "prompt": prompt,
            "output_format": "png",
            "aspect_ratio": "16:9"
        }
        
        # Make the API request
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/core",
            headers=headers,
            files={"none": ''},
            data=data
        )
        
        # Check the response status and handle the data
        if response.status_code == 200:
            # Assuming API returns image in the response; adjust as needed
            img_data = response.json().get('image')
            if num_img == 1:
                file_path = f"{img_dir}/{filename}.png"
            else:
                file_path = f"{img_dir}/{filename}_{index + 1:02d}.png"
                
            # Convert base64 to binary image and save
            with open(file_path, 'wb') as file:
                file.write(base64.b64decode(img_data))
            print(f"Saved image to {file_path}.")
        else:
            # Raise an exception with the response error
            raise Exception(f"Error for image {index + 1}: {response.json()}")