from openai import OpenAI
from dotenv import load_dotenv
from .break_down_article import get_article_and_chunks

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()

def paragraph_to_sentence(paragraph):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a summarizer who can summarize a chunk of text into a few sentences. You are great at getting the main theme"},
            {"role": "user", "content": f"Summarize this chunk of text into a few sentences. Only return a summary and nothing else! Get the main idea from it: {paragraph}"}
        ]
    )
    return response.choices[0].message.content

def summarize_until_under_limit(text, max_words):
    if len(text.split()) <= max_words:
        return text
    else:
        summary = paragraph_to_sentence(text)
        return summarize_until_under_limit(summary, max_words)

def article_to_paragraph(url, max_words=500):
    article_title, chunks = get_article_and_chunks(url)
    
    aggregated_summary = ""
    
    for chunk in chunks:
        summary = paragraph_to_sentence(chunk)
        aggregated_summary += summary + " "
    
    # If the aggregated summary exceeds the word limit, recursively summarize it until it doesn't
    final_summary = summarize_until_under_limit(aggregated_summary, max_words)
    
    return final_summary, article_title

def link_summary(url):
    summary, article_title = article_to_paragraph(url)
    return summary, article_title
    

def main():
    article_link = input("Enter the link to the article: ")
    summary, article_title = link_summary(article_link)
    print(f"Article Title: {article_title}")
    print(f"Summary: {summary}")

if __name__ == "__main__":
    main()