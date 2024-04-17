import json

def count_words_in_article(article):
    if isinstance(article, str):
        try:
            article = json.loads(article)
        except json.JSONDecodeError:
            print("Failed to decode JSON.")
            return False
    # Initialize word count
    word_count = 0

    # Helper function to count words in a single string
    def count_words(text):
        words = text.split()
        return len(words)

    # Count words in the main article title and intro
    word_count += count_words(article['article_title'])
    word_count += count_words(article['intro'])

    # Count words in each body section
    for section in article['body']:
        word_count += count_words(section['heading_title'])
        word_count += count_words(section['heading_text'])
        # Check for subheadings and count their words
        if 'subheadings' in section:
            for subheading in section['subheadings']:
                word_count += count_words(subheading['subheading_title'])
                word_count += count_words(subheading['subheading_text'])

    # Count words in the conclusion title and text
    word_count += count_words(article['conclusion_title'])
    word_count += count_words(article['conclusion'])
    
    return int(word_count)