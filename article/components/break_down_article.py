from .read_link import get_article
import re

def split_text_into_chunks(text):
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    # Initialize variables
    chunks = []
    current_chunk = ""
    word_count = 0

    # Iterate through sentences and construct new chunks
    for sentence in sentences:
        current_chunk += sentence + " "
        word_count += len(sentence.split())
        
        # If word count exceeds 500, start a new chunk
        if word_count >= 500:
            chunks.append(current_chunk.strip())
            current_chunk = ""
            word_count = 0

    # Add the last remaining part of the text if any
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def get_article_and_chunks(url):
    try:
        # Get article title and text
        article_title, article_text = get_article(url)
        
        # Split the article into chunks
        chunks = split_text_into_chunks(article_text)
        
        return article_title, chunks
    except Exception as e:
        print(f"Error getting article and chunks: {e}")
        return None, None

def main():
    try:
        # Ask the user to input the article link
        url = input("Please insert the article link: ")
        
        # Get article title and chunks
        if url:
            article_title, chunks = get_article_and_chunks(url)
            if article_title:
                print(f"Article Title: {article_title}")
                if chunks:
                    print("Chunks of approximately 500 words:")
                    for i, chunk in enumerate(chunks, 1):
                        print(f"{i}. {chunk}")
                else:
                    print("No chunks found.")
            else:
                print("Article title not available.")
        else:
            print("URL is required.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()