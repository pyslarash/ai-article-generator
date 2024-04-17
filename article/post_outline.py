import sys
sys.path.append('components')
import os
from openai import OpenAI
from dotenv import load_dotenv
from .components.link_paraphrase import article_to_paragraph
from .components.request_type_string import outline_request_type_string
import math
import re
import json

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()

gpt_engine = os.getenv("MAIN_CHAT_GPT_ENGINE")
temp = float(os.getenv("TEMPERATURE"))
freq_pen = float(os.getenv("FREQUENCY_PENALTY"))
pres_pen = float(os.getenv("PRESENCE_PENALTY"))
            
def headings_calculator(words):
    # Calculate total words in the article (excluding intro and conclusion)
    if words <= 1000: 
        total_words = words - 260
    else:
        total_words = words - 540
    
    # Check if subheadings are needed
    if words <= 1000:
        headings_needed = math.ceil(total_words / 260)
        return headings_needed, 0
    else:
        # Calculate total number of headings and subheadings
        total_headings_subheadings = math.ceil(total_words / 260)
        
        # Calculate number of headings
        headings_needed = math.ceil(total_headings_subheadings * 0.3)
        
        # Calculate number of subheadings
        subheadings_needed = (total_headings_subheadings - headings_needed) // headings_needed
        
        # Adjust subheadings to ensure there are at most 3 subheadings per heading
        while subheadings_needed > headings_needed * 3:
            subheadings_needed -= 1
        
        return headings_needed, subheadings_needed

def generate_outline(response):
    print("Creating an outline")
    sections = re.split(r'\n(?=\d+\.)', response.strip())
    outline = {"headings": []}
    
    for section in sections:
        if section.strip():
            lines = section.strip().split('\n')
            title = re.sub(r'^\s*[\dA-Za-z]+[\)\.]\s*', '', lines[0]).strip()
            
            heading = {
                "heading_title": title,
                "heading_text": "",
                "subheadings": []
            }

            for line in lines[1:]:
                if line.strip():
                    subheading_title = re.sub(r'^\s*[\dA-Za-z]+[\)\.]\s*', '', line).strip()
                    subheading = {
                        "subheading_title": subheading_title,
                        "subheading_text": ""
                    }
                    heading["subheadings"].append(subheading)

            outline["headings"].append(heading)

    return json.dumps(outline, indent=4)

# This function rewrites an existing post using your keyword
def post_outline_article_rewrite(url, words, keyword, meaning, voice_type):
    print("Starting to rewrite an article...")
    headings, subheadings = headings_calculator(words)
    summary = article_to_paragraph(url)
    request_type = "article-rewrite"
    bot_role, extra_data = outline_request_type_string(request_type, summary, keyword)
    if subheadings == 0:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings. Please, number your headings with regular numbers (not roman numerals). "
                            f"You MUST include this keyword '{keyword}' in one of the headings. Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings and {subheadings} subheadings under each of the headings. "
                            f"Please, number your headings with regular numbers (not roman numerals) and put letters in front of subheadings. "
                            f"You MUST include this keyword '{keyword}' in ONE OF THE HEADINGS and ONE OF THE SUBHEADINGS. "
                            f"Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    # Extracting the text from the response correctly
    text = response.choices[0].message.content
    outline_json = generate_outline(text)
    return request_type, outline_json, summary, text

# This function creates a new post based on the topic you provide
def post_outline_topic(topic, words, keyword, meaning, voice_type):
    print("Starting to write an article based on a topic...")
    headings, subheadings = headings_calculator(words)
    request_type = "topic"
    bot_role, extra_data = outline_request_type_string(request_type, topic, keyword)
    if subheadings == 0:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"{extra_data}"
                            f"Make it not detectable by the GPT detectors (do everything you can for it!) "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings. "
                            f"Please, number your headings with regular numbers (not roman numerals). "
                            f"You MUST include this keyword '{keyword}' in one of the headings. "
                            f"Do not write anything else, but them."
                }
            ]
        )
    else:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"{extra_data}"
                            f"Make it not detectable by the GPT detectors (do everything you can for it!) "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings and {subheadings} subheadings under each of the headings. "
                            f"Please, number your headings with regular numbers (not roman numerals) and put letters in front of subheadings. "
                            f"You MUST include this keyword '{keyword}' in one of the headings and one of the subheadings. "
                            f"Do not write anything else, but them."
                }
            ]
        )
    # Extracting the text from the response correctly
    text = response.choices[0].message.content
    outline_json = generate_outline(text)
    return request_type, outline_json, topic, text

# This function discusses the product you'd like to write about
def post_outline_single_product_promo(url, words, keyword, meaning, voice_type):
    print("Starting to create a single product promo...")
    headings, subheadings = headings_calculator(words)
    summary = article_to_paragraph(url)
    request_type = "single-product-promo"
    bot_role, extra_data = outline_request_type_string(request_type, summary, keyword)
    if subheadings == 0:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings. "
                            f"Please, number your headings with regular numbers (not roman numerals). "
                            f"You MUST include this keyword '{keyword}' in one of the headings. "
                            f"Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings and {subheadings} subheadings under each of the headings. "
                            f"Please, number your headings with regular numbers (not roman numerals) and put letters in front of subheadings. "
                            f"You MUST include this keyword '{keyword}' in ONE OF THE HEADINGS and ONE OF THE SUBHEADINGS. "
                            f"Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    # Extracting the text from the response correctly
    text = response.choices[0].message.content
    outline_json = generate_outline(text)
    return request_type, outline_json, summary, text

# This function promotes multiple products in your post
def post_outline_multiple_products_promo(urls, words, keyword, meaning, voice_type):
    print("Starting to write a multi-product promo...")
    summaries = []
    for url in urls:
        headings, subheadings = headings_calculator(words)
        summary = article_to_paragraph(url)
        summaries.append(summary)
    
    # Constructing the string with numbered summaries
    summary_string = ""
    for i, summary in enumerate(summaries, start=1):
        summary_string += f"Summary {i}: {summary}; "
    request_type = "multi-product-promo"
    bot_role, extra_data = outline_request_type_string(request_type, summary, keyword)
    if subheadings == 0:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings. "
                            f"Please, number your headings with regular numbers (not roman numerals). "
                            f"You MUST include this keyword '{keyword}' in one of the headings. "
                            f"Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings and {subheadings} subheadings under each of the headings. "
                            f"Please, number your headings with regular numbers (not roman numerals) and put letters in front of subheadings. "
                            f"You MUST include this keyword '{keyword}' in ONE OF THE HEADINGS and ONE OF THE SUBHEADINGS. "
                            f"Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    # Extracting the text from the response correctly
    text = response.choices[0].message.content
    outline_json = generate_outline(text)
    return request_type, outline_json, summary_string, text

# This function promotes multiple products in your post
def post_outline_topic_and_info(topic, urls, words, keyword, meaning, voice_type):
    print("Starting to write an article based on a topic and information...")
    summaries = []
    for url in urls:
        headings, subheadings = headings_calculator(words)
        summary = article_to_paragraph(url)
        summaries.append(summary)
    
    # Constructing the string with numbered summaries
    summary_string = ""
    for i, summary in enumerate(summaries, start=1):
        summary_string += f"Summary {i}: {summary}; "
    request_type = "topic-and-information"
    bot_role, extra_data = outline_request_type_string(request_type, summary, keyword)
    if subheadings == 0:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"You are writing an outline based on this topic: {topic}"
                            f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings. "
                            f"Please, number your headings with regular numbers (not roman numerals). "
                            f"You MUST include this keyword '{keyword}' in one of the headings. "
                            f"Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
            model=gpt_engine,
            temperature=temp,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            messages = [
                {"role": "system", "content": bot_role},
                {
                    "role": "user",
                    "content": f"You are writing an outline based on this topic: {topic}"
                            f"Create an outline for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                            f"You are writing a {meaning} type of the post using {voice_type} voice. "
                            f"You will NOT have to create a heading for introduction or conclusion! "
                            f"You only have to provide {headings} headings and {subheadings} subheadings under each of the headings. "
                            f"Please, number your headings with regular numbers (not roman numerals) and put letters in front of subheadings. "
                            f"You MUST include this keyword '{keyword}' in ONE OF THE HEADINGS and ONE OF THE SUBHEADINGS. "
                            f"Do not write anything else, but them. "
                            f"{extra_data}"
                }
            ]
        )
    # Extracting the text from the response correctly
    text = response.choices[0].message.content
    outline_json = generate_outline(text)
    return request_type, outline_json, summary_string, text