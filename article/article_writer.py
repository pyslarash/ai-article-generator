import sys
import re
import os
import json
sys.path.append('components')
from openai import OpenAI
from dotenv import load_dotenv
from .components.previous_paraphrase import previous_paraphrase
from .components.keyword_density_check import keyword_density
from .intro_writer import intro_writer
from .conclusion_writer import conclusion_writer
from .components.parse_json import parse_json
from .components.gpt_intro_conclusion_writing_prompts import write_article_title
from .components.request_type_string import request_type_string
from .components.gpt_writing_prompts import (write_two_heading_paragraphs_original, rewrite_two_heading_paragraphs_if_kw_density_low, rewrite_two_heading_paragraphs_if_kw_density_high,
                                            write_two_subheading_paragraphs_original, rewrite_two_subheading_paragraphs_if_kw_density_low, 
                                            rewrite_two_subheading_paragraphs_if_kw_density_high)

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()
gpt_engine = os.getenv("MAIN_CHAT_GPT_ENGINE")

previous_summary = None

def remove_text_before_title(sub_text, title):
    # Attempt to remove the title at the beginning with optional formatting
    title_pattern = rf"^\s*[\*\*]*{re.escape(title)}[\*\*]*[!?:]*\s*"
    pattern = re.compile(title_pattern)
    match = pattern.match(sub_text)
    if match:
        # Remove title and any following whitespace/newlines
        return sub_text[match.end():].lstrip()

    # Clean up common formatting issues and introductory phrases at the beginning of the text
    cleanup_pattern = re.compile(r"^\s*[\*\*]*\s*(Paragraphs:|Introduction:|Summary:)?\s*")
    sub_text = cleanup_pattern.sub('', sub_text)
    return sub_text

def article_writer(json_data, keyword, request_type, additional_data, meaning, voice):
    global previous_summary  # Access the global variable
    outline_result = parse_json(json_data)
    
    if outline_result is None:
        print("No valid JSON outline data found in article_writer.py.")
        return {}, None
    else:
        print("JSON data processed successfully.")
    
    if isinstance(json_data, str):
        outline_data = json.loads(json_data)  # Deserialize string to dictionary
    else:
        outline_data = json_data  # Already a dictionary, use directly
    
    bot_role, extra_data = request_type_string(request_type, additional_data, keyword)
    generated_texts = {}
    all_text = ""

    max_retries = 5  # Set a maximum number of retries to avoid infinite loops

    if 'headings' in outline_data:
        for heading in outline_data['headings']:
            heading_title = heading['heading_title']
            subheadings = heading['subheadings']
            
            heading_text = None
            subheading_texts = {}
            retries = 0

            while retries < max_retries:
                heading_text = write_two_heading_paragraphs_original(bot_role, meaning, voice, heading_title, keyword, extra_data, previous_summary)
                print(f"Writing heading - Attempt {retries + 1} out of {max_retries}")
                density_status = keyword_density(heading_text, keyword)
                if density_status == "low":
                    heading_text = rewrite_two_heading_paragraphs_if_kw_density_low(bot_role, meaning, voice, heading_title, keyword, heading_text, previous_summary)
                    print("Keyword density low. Rewriting heading text.")
                elif density_status == "high":
                    heading_text = rewrite_two_heading_paragraphs_if_kw_density_high(bot_role, meaning, voice, heading_title, keyword, heading_text, previous_summary)
                    print("Keyword density high. Rewriting heading text.")
                else:
                    print("Keyword density is OK!")
                    break  # Exit loop if density is acceptable

                retries += 1
            if retries == max_retries:
                print("Failed to achieve desired keyword density after maximum retries for heading.")

            # Generate text for subheadings similarly
            for subheading_data in subheadings:
                subheading_title = subheading_data['subheading_title']
                subheading_text = None
                sub_retries = 0

                while sub_retries < max_retries:
                    subheading_text = write_two_subheading_paragraphs_original(bot_role, meaning, voice, keyword, subheading_title, heading_text, extra_data, previous_summary)
                    print(f"Writing subheading - Attempt {sub_retries + 1} out of {max_retries}")
                    if keyword_density(subheading_text, keyword) == "low":
                        subheading_text = rewrite_two_subheading_paragraphs_if_kw_density_low(bot_role, meaning, voice, subheading_title, keyword, subheading_text, previous_summary)
                        print("Keyword density low. Rewriting subheading text.")
                    elif keyword_density(subheading_text, keyword) == "high":
                        subheading_text = rewrite_two_subheading_paragraphs_if_kw_density_high(bot_role, meaning, voice, subheading_title, keyword, subheading_text, previous_summary)
                        print("Keyword density high. Rewriting subheading text.")
                    else:
                        print("Keyword density is OK!")
                        break  # Acceptable density

                    sub_retries += 1
                if sub_retries == max_retries:
                    print("Failed to achieve desired keyword density after maximum retries for subheading.")

                subheading_texts[subheading_title] = subheading_text

            generated_texts[heading_title] = {
                "heading_title": heading_title,
                "heading_text": heading_text,
                "subheadings": subheading_texts
            }

            # Add to all_text
            all_text += heading_text + " " + " ".join(subheading_texts.values())

    summarized_text = previous_paraphrase(previous_summary, all_text, gpt_engine)
    previous_summary = summarized_text
    print("Article body successfully generated")

    return generated_texts, summarized_text

def full_json_article(generated_texts, summarized_text, words, keyword, voice, meaning, unedited_outline):
    # Generate the title
    title = write_article_title(summarized_text, keyword, unedited_outline, meaning, voice)
    print("Title generated")
    # Generate the introduction
    intro = intro_writer(words, summarized_text, keyword, voice, meaning)
    print("Intro generated")
    # Generate the conclusion
    conclusion, conclusion_title = conclusion_writer(words, summarized_text, keyword, voice, meaning)
    print("Conclusion generated")
    # Create a new JSON object for the modified article
    modified_json = {
        "article_title": title,
        "intro": intro,
        "body": []
    }

    # Add the main content from generated_texts
    for heading_title, heading_content in generated_texts.items():
        heading_data = {
            "heading_title": heading_title,
            "heading_text": heading_content["heading_text"],
            "subheadings": []
        }

        # Add subheadings
        for subheading_title, subheading_text in heading_content["subheadings"].items():
            subheading_data = {
                "subheading_title": subheading_title,
                "subheading_text": subheading_text
            }
            heading_data["subheadings"].append(subheading_data)

        modified_json["body"].append(heading_data)

    # Add the conclusion title and content
    modified_json["conclusion_title"] = conclusion_title
    modified_json["conclusion"] = conclusion        
    print("JSON of the article successfully created")
    return modified_json

def save_json_to_file(json_data, filename):
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=4)