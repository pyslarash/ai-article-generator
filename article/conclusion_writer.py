import sys
import os
import json
sys.path.append('components')
from openai import OpenAI
from dotenv import load_dotenv
from .components.keyword_density_check import keyword_density
from .components.zerogpt_check import zerogpt_check
from .components.originality_check import originality_check
from .components.gpt_intro_conclusion_writing_prompts import (write_conclusion_paragraph, rewrite_conclusion_paragraph_if_kw_density_low,
                                                             rewrite_conclusion_paragraph_if_kw_density_high, write_conclusion_title)

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()
gpt_engine = os.getenv("MAIN_CHAT_GPT_ENGINE")
max_retries = 5

def conclusion_writer(words, summary, keyword, voice, meaning, max_retries=5):
    passed_keyword_density_check = False
    attempt_count = 0  # Initialize retry counter

    while not passed_keyword_density_check and attempt_count < max_retries:
        # Generate text for the conclusion
        previous_text = write_conclusion_paragraph(words, summary, keyword, voice, meaning)
        print(f"Writing conclusion - Attempt {attempt_count + 1} out of {max_retries}")

        # Check keyword density and decide if rewrites are needed
        density_status = keyword_density(previous_text, keyword)

        if density_status == "low":
            previous_text = rewrite_conclusion_paragraph_if_kw_density_low(words, previous_text, keyword, voice, meaning)
            print("Keyword density low. Rewriting conclusion with higher density.")
        elif density_status == "high":
            previous_text = rewrite_conclusion_paragraph_if_kw_density_high(words, previous_text, keyword, voice, meaning)
            print("Keyword density high. Rewriting conclusion with lower density.")
        else:
            passed_keyword_density_check = True  # Correct density achieved

        attempt_count += 1  # Increment attempt counter

    if attempt_count == max_retries:
        print(f"Max retries reached ({max_retries}). Using last modified conclusion.")
    
    print("Keyword density is OK!")
    # Generate and clean the title for the conclusion
    conclusion_title = write_conclusion_title(previous_text)
    conclusion_title = conclusion_title.strip('"')  # Remove surrounding quotes if any
    
    return previous_text, conclusion_title