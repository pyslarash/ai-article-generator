import sys
import os
import json
sys.path.append('components')
from openai import OpenAI
from dotenv import load_dotenv
from .components.keyword_density_check import keyword_density
from .components.zerogpt_check import zerogpt_check
from .components.originality_check import originality_check
from .components.gpt_intro_conclusion_writing_prompts import (write_introduction_paragraph, rewrite_introduction_paragraph_if_kw_density_low,
                                                             rewrite_introduction_paragraph_if_kw_density_high)

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()
gpt_engine = os.getenv("MAIN_CHAT_GPT_ENGINE")
max_retries = 5

def intro_writer(words, summary, keyword, voice, meaning, max_retries=5):
    passed_keyword_density_check = False
    attempt_count = 0  # Initialize retry counter

    while not passed_keyword_density_check and attempt_count < max_retries:
        # Generate text for the introduction
        previous_text = write_introduction_paragraph(words, summary, keyword, voice, meaning)
        print(f"Writing introduction - Attempt {attempt_count + 1} out of {max_retries}")
        
        # Check keyword density and decide if rewrites are needed
        density_status = keyword_density(previous_text, keyword)

        if density_status == "low":
            previous_text = rewrite_introduction_paragraph_if_kw_density_low(words, previous_text, keyword, voice, meaning)
            print("Keyword density low. Rewriting introduction with higher density.")
        elif density_status == "high":
            previous_text = rewrite_introduction_paragraph_if_kw_density_high(words, previous_text, keyword, voice, meaning)
            print("Keyword density high. Rewriting introduction with lower density.")
        else:
            passed_keyword_density_check = True  # Correct density achieved

        attempt_count += 1  # Increment attempt counter

    if attempt_count == max_retries:
        print(f"Max retries reached ({max_retries}). Using last modified introduction.")
    
    print("Keyword density is OK!")
    return previous_text