import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()
gpt_engine = os.getenv("MAIN_CHAT_GPT_ENGINE")
temp = float(os.getenv("TEMPERATURE"))
freq_pen = float(os.getenv("FREQUENCY_PENALTY"))
pres_pen = float(os.getenv("PRESENCE_PENALTY"))

def rewrite_paragraph(keyword, text):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an outstanding AI detection obfuscator who writes amazing human-like text based on the existing paragraph."},
            {
            "role": "user",
            "content": f"You need to utilize this keyword in this paragraph aiming for 1.5% keyword density: {keyword}"
                    f"Rewrite this text to be completely undetectable by AI checkers. Use human-like voice: {text} "
            }
        ]
    )
    return response.choices[0].message.content

def main():
    keyword = input("What is the focus keyword? ")
    text = input("Enter the text we need to rewrite: ")
    print("Here is the new paragraph:")
    print(rewrite_paragraph(keyword, text))
    
if __name__ == "__main__":
    main()