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

rules_file="rules.txt"
with open(rules_file, 'r') as file:
    rules = file.read()

# This function writes the two first paragraphs
def minimize_heading_paragraphs_original(bot_role, meaning, voice, keyword, extra_data, paragraph):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=0.43,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"You just wrote this text: {paragraph} "
                        f"The problem is it is way too long. We need to make it shorter! "
                        f"Minimize 2 paragraphs for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword}"
                        f"{extra_data}"
            }
            ]
        )    
    return response.choices[0].message.content

# This function rewrites the two first paragraphs if the keyowrd density was low
def minimize_heading_paragraphs_if_kw_density_low(bot_role, meaning, voice, keyword, heading_text):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"You just wrote this text, but the keyword density was too low: {heading_text}"
                        f"Rewrite the heading for a blog post that's not detectable by the GPT detectors (do everything you can for it!) with a slightly HIGHER keyword density. "
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! Keep the length of the text about the same. "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# This function rewrites the two first paragraphs if the keyowrd density was high
def minimize_heading_paragraphs_if_kw_density_high(bot_role, meaning, voice, keyword, heading_text):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"You just wrote this heading, but the keyword density was too high: {heading_text}"
                        f"Rewrite the heading for a blog post that's not detectable by the GPT detectors (do everything you can for it!) with a slightly LOWER keyword density. "
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! Keep the length of the text about the same. "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# Writes two original subheading paragraphs under the first heading
def minimize_subheading_paragraphs_original(bot_role, meaning, voice, keyword, extra_data, paragraph):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"You just wrote this text: {paragraph} "
                        f"The problem is it is way too long. We need to make it shorter! "
                        f"Minimize 2 paragraphs for a blog post that's not detectable by the GPT detectors (do everything you can for it!)."
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword}"
                        f"{extra_data}"
            }
        ]
    )
    return response.choices[0].message.content

# Rewrites two subhead paragraphs under the first heading if kw density is low
def minimize_subheading_paragraphs_if_kw_density_low(bot_role, meaning, voice, keyword, subheading_text):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"You just wrote these 2 paragraphs, but the keyword density was too low: {subheading_text}"
                f"Rewrite 2 paragraphs for a blog post that's not detectable by the GPT detectors (do everything you can for it!) with a slightly higher keyword density. "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"Only return the paragraphs and nothing else! Keep the length of the text about the same. "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# Rewrites two subhead paragraphs under the first heading if kw density is high
def minimize_subheading_paragraphs_if_kw_density_high(bot_role, meaning, voice, keyword, subheading_text):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"You just wrote these 2 paragraphs, but the keyword density was too high: {subheading_text}"
                    f"Rewrite 2 paragraphs for a blog post that's not detectable by the GPT detectors (do everything you can for it!) with a slightly lower keyword density. "
                    f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                    f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                    f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                    f"Only return the paragraphs and nothing else! Keep the length of the text about the same. "
                    f"You are writing a {meaning} type of the post using {voice} voice. "
                    f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content