import os
import json
from .gpt_rewriting_prompts import (minimize_heading_paragraphs_original, minimize_heading_paragraphs_if_kw_density_low,
                                   minimize_heading_paragraphs_if_kw_density_high, minimize_subheading_paragraphs_original, 
                                   minimize_subheading_paragraphs_if_kw_density_low, minimize_subheading_paragraphs_if_kw_density_high)
from .word_count import count_words_in_article
from ..article_writer import remove_text_before_title
from openai import OpenAI
from dotenv import load_dotenv
from .request_type_string import request_type_string
from .keyword_density_check import keyword_density
from .parse_json import parse_json

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()
gpt_engine = os.getenv("MAIN_CHAT_GPT_ENGINE")

def fit_to_word_limit(json_data, keyword, request_type, additional_data, meaning, voice, hard_limit):
    article = json.loads(json_data)
    result = parse_json(json_data)
    
    if result is None:
        print("No valid JSON data found in minimize_article.py fit_to_word_limit.")
    else:
        print("JSON data processed successfully.")
    current_word_count = count_words_in_article(article)
    bot_role, extra_data = request_type_string(request_type, additional_data, keyword)
    
    while current_word_count > hard_limit:
        for section in article['body']:
            passed_checks = False
            while not passed_checks:
                heading_text = section['heading_text']
                # Check and rewrite heading text
                heading_text = rewrite_headings_based_on_checks(heading_text, section['heading_title'], bot_role, meaning, voice, keyword, extra_data)
                section['heading_text'] = remove_text_before_title(heading_text, section['heading_title'])  # Correct variable
                
                # Process each subheading
                for subheading in section['subheadings']:
                    subheading_text = subheading['subheading_text']
                    subheading_text = rewrite_subheadings_based_on_checks(subheading_text, subheading['subheading_title'], bot_role, meaning, voice, keyword, extra_data)
                    subheading['subheading_text'] = remove_text_before_title(subheading_text, subheading['subheading_title'])  # Correct variable

                current_word_count = count_words_in_article(article)
                if current_word_count <= hard_limit:
                    passed_checks = True
                    break
    
    modified_json = json.dumps(article)
    save_json_to_file(modified_json, 'shrinked_article.json')
    return modified_json

def rewrite_headings_based_on_checks(text, title, bot_role, meaning, voice, keyword, extra_data):
    modified_text = minimize_heading_paragraphs_original(bot_role, meaning, voice, keyword, extra_data, text)
    keyword_result = keyword_density(modified_text, keyword)
    if keyword_result == "low":
        modified_text = minimize_heading_paragraphs_if_kw_density_low(bot_role, meaning, voice, keyword, modified_text)
    elif keyword_result == "high":
        modified_text = minimize_heading_paragraphs_if_kw_density_high(bot_role, meaning, voice, keyword, modified_text)

    return modified_text

def rewrite_subheadings_based_on_checks(text, title, bot_role, meaning, voice, keyword, extra_data):
    modified_text = minimize_subheading_paragraphs_original(bot_role, meaning, voice, keyword, extra_data, text)
    keyword_result = keyword_density(modified_text, keyword)
    if keyword_result == "low":
        modified_text = minimize_subheading_paragraphs_if_kw_density_low(bot_role, meaning, voice, keyword, modified_text)
    elif keyword_result == "high":
        modified_text = minimize_subheading_paragraphs_if_kw_density_high(bot_role, meaning, voice, keyword, modified_text)

    return modified_text

def save_json_to_file(json_data, filename):
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=4)