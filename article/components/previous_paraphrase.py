from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()

def previous_paraphrase(previous_summary, new_text, gpt_engine):
    if gpt_engine == "gpt-4-turbo":
        if previous_summary is None:
            existing = ""
        else:
            existing = previous_summary
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a blog writer who needs to summarize previous written text of your article. You are great at getting the main theme"},
                {"role": "user",
                "content": f"Summarize this chunk of text into a few paragraphs. Only return a summary and nothing else! "
                            f"This is the text that you just wrote and need to add to existing summary: {new_text} "
                            f"If you already summarized some previous text before the new text, it's here: {existing}"
                
                }
            ]
        )
    elif gpt_engine == "gpt-3.5-turbo-0125":
        if previous_summary is None:
            existing = ""
        else:
            existing = previous_summary
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a blog writer who needs to summarize previous written text of your article. You are great at getting the main theme"},
                {"role": "user",
                "content": f"Summarize this chunk of text into a few sentences. Only return a summary and nothing else! "
                            f"This is the text that you just wrote and need to add to existing summary: {new_text} "
                            f"If you already summarized some previous text before the new text, it's here: {existing}"
                
                }
            ]
        )
    else: print("Error in previous_paraphrase.py")
    
    return response.choices[0].message.content