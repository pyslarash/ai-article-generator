from newspaper import Article

def extract_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text
    except Exception as e:
        return f"Error: {e}"

def get_article(url):
    try:
        title, article_text = extract_article(url)
        return title, article_text
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None, None

def main():
    try:
        # Ask the user to input the article link
        url = input("Please insert the article link: ")
        
        # Get the article text and title
        title, article_text = get_article(url)
        
        # Print the title and article text
        if title and article_text:
            print(f"Title: {title}")
            print(f"\nArticle Text:\n{article_text}")
        else:
            print("Failed to retrieve article.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()