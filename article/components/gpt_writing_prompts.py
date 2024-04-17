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
def write_two_heading_paragraphs_original(bot_role, meaning, voice, heading, keyword, extra_data, previous_summary):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"Create 2 paragraphs for a blog post that's not detectable by the GPT detectors (do everything you can for it!)."
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "                        
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"The heading for these two paragraphs is: {heading}! "
                        f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword}"
                        f"{extra_data}"
            }
            ]
        )    
    return response.choices[0].message.content

# This function rewrites the two first paragraphs if the keyowrd density was low
def rewrite_two_heading_paragraphs_if_kw_density_low(bot_role, meaning, voice, heading, keyword, heading_text, previous_summary):
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
                        f"Rewrite the text for a blog post that's not detectable by the GPT detectors (do everything you can for it!) with a slightly HIGHER keyword density. "
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"The heading for this is: {heading}! "
                        f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# This function rewrites the two first paragraphs if the keyowrd density was high
def rewrite_two_heading_paragraphs_if_kw_density_high(bot_role, meaning, voice, heading, keyword, heading_text, previous_summary):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"You just wrote this text, but the keyword density was too high: {heading_text}"
                        f"Rewrite the text for a blog post that's not detectable by the GPT detectors (do everything you can for it!) with a slightly LOWER keyword density. "
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"The heading for this is: {heading}! "
                        f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# This function rewrites the two first paragraphs if the AI check has failed
def rewrite_two_heading_paragraphs_if_ai_check_failed(bot_role, meaning, voice, heading, keyword, heading_text, previous_summary):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"This text is being detected by the AI detectors: {heading_text}"
                f"Rewrite the text for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                f"Utilize words that are less likely to be used by the AI. Maybe, use more slang or idiomatic expressions and make it sound more human-like. "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"The heading for this is: {heading}! "
                f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# Writes two original subheading paragraphs under the first heading
def write_two_subheading_paragraphs_original(bot_role, meaning, voice, keyword, subheading, heading_text, extra_data, previous_summary):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
                "role": "user",
                "content": f"Create 2 paragraphs for a blog post that's not detectable by the GPT detectors (do everything you can for it!)."
                        f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                        f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                        f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                        f"Only return the paragraphs and nothing else! "
                        f"You are writing a {meaning} type of the post using {voice} voice. "
                        f"The subheading for these two paragraphs is: {subheading}! "
                        f"This is what you wrote in the heading already: {heading_text}! "
                        f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                        f"This is the keyword for this article (aim for 1.5% keyword density): {keyword}"
                        f"{extra_data}"
            }
        ]
    )
    return response.choices[0].message.content

# Rewrites two subhead paragraphs under the first heading if kw density is low
def rewrite_two_subheading_paragraphs_if_kw_density_low(bot_role, meaning, voice, subheading, keyword, subheading_text, previous_summary):
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
                f"Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"The subheading for these two paragraphs is: {subheading}! "
                f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# Rewrites two subhead paragraphs under the first heading if kw density is high
def rewrite_two_subheading_paragraphs_if_kw_density_high(bot_role, meaning, voice, subheading, keyword, subheading_text, previous_summary):
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
                    f"Only return the paragraphs and nothing else! "
                    f"You are writing a {meaning} type of the post using {voice} voice. "
                    f"The subheading for these two paragraphs is: {subheading}! "
                    f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                    f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content

# Rewrites two subhead paragraphs under the first heading if didn't pass the AI check
def rewrite_two_subheading_paragraphs_if_ai_check_failed(bot_role, meaning, voice, subheading, keyword, subheading_text, previous_summary):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": bot_role},
            {
            "role": "user",
            "content": f"You just wrote these 2 paragraphs, but they are being detected by the AI detectors: {subheading_text}"
                    f"Rewrite 2 paragraphs for a blog post that's not detectable by the GPT detectors (do everything you can for it!). "
                    f"Utilize words that are less likely to be used by the AI. Maybe, use more slang or idiomatic expressions and make it sound more human-like. "
                    f"Sprinkle in some idioms or conversational tone if needed. "
                    f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                    f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                    f"Only return the paragraphs and nothing else! "
                    f"You are writing a {meaning} type of the post using {voice} voice. "
                    f"The subheading for these two paragraphs is: {subheading}! "
                    f"If there was something written in this article already, here's the summary that you can refer to: {previous_summary} "
                    f"This is the keyword for this article (aim for 1.5% keyword density): {keyword} "
            }
        ]
    )
    return response.choices[0].message.content