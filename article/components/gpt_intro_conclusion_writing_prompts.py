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
    
# Introductory paragraph(s) part
def write_introduction_paragraph(words, summary, keyword, voice, meaning):
    if words <= 1000:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to write a single intro paragraph based on a summary of an article."},
            {
            "role": "user", "content": f"Write a single intro paragraph based on a summary of an article. Only return the paragraph and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this paragraph that you must include in the first sentence (aim for 1.5% keyword density): {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the summary of the article: {summary} "
                }
            ]
        )
    else:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to write two intro paragraphs based on a summary of an article."},
            {
            "role": "user", "content": f"Write two intro paragraphs based on a summary of an article. Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for the paragraphs that you must include in the first sentence (aim for 1.5% keyword density): {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the summary of the article: {summary} "
                }
            ]
        )
    return response.choices[0].message.content

def rewrite_introduction_paragraph_if_kw_density_low(words, previous_text, keyword, voice, meaning):
    if words <= 1000:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite a single intro paragraph based on already-written paragraph."},
            {
            "role": "user", "content": f"You need to rewrite an already-written paragraph beacuse the keyword density was too low. Only return the paragraph and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this paragraph that you must include in the first sentence (aim for 1.5% keyword density) and increase the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite two intro paragraphs based on already-written paragraphs."},
            {
            "role": "user", "content": f"You need to rewrite two already-written paragraphs beacuse the keyword density was too low. Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for the paragraphs that you must include in the first sentence (aim for 1.5% keyword density) and increase the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    return response.choices[0].message.content

def rewrite_introduction_paragraph_if_kw_density_high(words, previous_text, keyword, voice, meaning):
    if words <= 1000:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite a single intro paragraph based on already-written paragraph."},
            {
            "role": "user", "content": f"You need to rewrite an already-written paragraph beacuse the keyword density was too high. Only return the paragraph and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this paragraph that you must include in the first sentence (aim for 1.5% keyword density) and decrease the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite two intro paragraphs based on already-written paragraphs."},
            {
            "role": "user", "content": f"You need to rewrite two already-written paragraphs beacuse the keyword density was too high. Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for the paragraphs that you must include in the first sentence (aim for 1.5% keyword density) and decrease the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    return response.choices[0].message.content

# Conclusion paragraph(s) part
def write_conclusion_paragraph(words, summary, keyword, voice, meaning):
    if words <= 1000:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to write a single comclusion paragraph based on a summary of an article."},
            {
            "role": "user", "content": f"Write a single comclusion paragraph based on a summary of an article. Only return the paragraph and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this paragraph that you must include in the first sentence (aim for 1.5% keyword density): {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the summary of the article: {summary} "
                }
            ]
        )
    else:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to write two comclusion paragraphs based on a summary of an article."},
            {
            "role": "user", "content": f"Write two comclusion paragraphs based on a summary of an article. Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this paragraph that you must include in the first sentence (aim for 1.5% keyword density): {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the summary of the article: {summary} "
                }
            ]
        )
    return response.choices[0].message.content

def rewrite_conclusion_paragraph_if_kw_density_low(words, previous_text, keyword, voice, meaning):
    if words <= 1000:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite a single conclusion paragraph based on already-written paragraph."},
            {
            "role": "user", "content": f"You need to rewrite an already-written paragraph beacuse the keyword density was too low. Only return the paragraph and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this paragraph that you must include in the first sentence (aim for 1.5% keyword density) and increase the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite two conclusion paragraphs based on already-written paragraphs."},
            {
            "role": "user", "content": f"You need to rewrite two already-written paragraphs beacuse the keyword density was too low. Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for the paragraphs that you must include in the first sentence (aim for 1.5% keyword density) and increase the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    return response.choices[0].message.content

def rewrite_conclusion_paragraph_if_kw_density_high(words, previous_text, keyword, voice, meaning):
    if words <= 1000:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite a single concluison paragraph based on already-written paragraph."},
            {
            "role": "user", "content": f"You need to rewrite an already-written paragraph beacuse the keyword density was too high. Only return the paragraph and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for this paragraph that you must include in the first sentence (aim for 1.5% keyword density) and decrease the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    else:
        response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to rewrite two conclusion paragraphs based on already-written paragraphs."},
            {
            "role": "user", "content": f"You need to rewrite two already-written paragraphs beacuse the keyword density was too high. Only return the paragraphs and nothing else! "
                f"You are writing a {meaning} type of the post using {voice} voice. "
                f"This is the keyword for the paragraphs that you must include in the first sentence (aim for 1.5% keyword density) and decrease the keyword density: {keyword} "
                f"Sprinkle in some idioms and some slang or conversational tone if needed. Make it sound human-like. "
                f"Write in a very personal style, use multiple literary devices, include slang and anecdotes! "
                f"Utilize these rules to avoid being detected by AI checkers: {rules}"
                f"This is the paragraph that you need to rewrite: {previous_text}"
                }
            ]
        )
    return response.choices[0].message.content

def write_conclusion_title(text):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to write a short catchy title for a conclusion paragraph."},
            {
            "role": "user", "content": f"Write a catchy title for this conclusion paragraph. Only include the title and nothing else! This is the paragraph: {text}"
                }
            ]
        )
    return response.choices[0].message.content

def write_article_title(summary, keyword, unedited_outline, meaning, voice):
    response = client.chat.completions.create(
        model=gpt_engine,
        temperature=temp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        messages=[
            {"role": "system", "content": "You are an SEO blog post writer who has to write a catchy title for a blog post!"},
            {
            "role": "user", 
                "content": f"Write a catchy title for a blog post utilizing this keyword: {keyword} "
                        f"This keyword is mandatory in the title!!! "
                        f"Do not use any quotation marks or anything around the title. Just provide the title. "
                        f"You are writing a {meaning} type of the title using {voice} voice. "
                        f"This is the outline of the article: {unedited_outline} "
                        f"This is the summary of an article: {summary}"
                }
            ]
        )
    return response.choices[0].message.content.strip('"')