def keyword_density(text, keyword):
    print("Checking keyword density")
    # Convert text to lowercase for case-insensitive comparison
    text_lower = text.lower()
    
    # Split text into words
    words = text_lower.split()
    
    # Count the number of occurrences of the keyword in the text
    keyword_count = text_lower.count(keyword.lower())
    
    # Calculate the total number of words in the text
    total_words = len(words)
    
    # Calculate keyword density
    density = (keyword_count / total_words) * 100
    
    # Check if keyword density is between 0.5% and 3%
    if 0.5 <= density <= 3:
        return True
    else:
        # Check if density is low or high
        if density < 0.5:
            return "low"
        else:
            return "high"