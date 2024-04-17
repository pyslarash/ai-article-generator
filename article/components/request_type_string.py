rules_file="rules.txt"
with open(rules_file, 'r') as file:
    rules = file.read()

# This function adjust prompts based on the type of article that has been requested by the user
def request_type_string(request_type, additional_data, keyword):
    if request_type == "article-rewrite":
        bot_role = f"""
        You are an SEO blog post writer who rewrites existing articles and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN THE TEXT WITH 1.5% KEYWORD DENSITY.
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the article you are rewriting: {additional_data}"
        return bot_role, extra_data
    elif request_type == "topic":
        bot_role = f"""
        You are an SEO blog post writer who writes articles based on a certain topic and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN THE TEXT WITH 1.5% KEYWORD DENSITY.
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the topic for your blog post: {additional_data}"
        return bot_role, extra_data
    elif request_type == "single-product-promo":
        bot_role = f"""
        You are an SEO blog post writer who discusses a certain product and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN THE TEXT WITH 1.5% KEYWORD DENSITY.
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the product page you are rewriting: {additional_data}"
        return bot_role, extra_data
    elif request_type == "multi-product-promo":
        bot_role = f"""
        You are an SEO blog post writer who talks about multiple products and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN THE TEXT WITH 1.5% KEYWORD DENSITY.
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the products you need to talk about: {additional_data}"
        return bot_role, extra_data
    elif request_type == "topic-and-information":
        bot_role = f"""
        You are an SEO blog post writer who talks about a certain topic, uses provided information, and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN THE TEXT WITH 1.5% KEYWORD DENSITY.
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the information that you should add in your article: {additional_data}"
        return bot_role, extra_data
    else:
        return ("There is an error in request_type_string.py file")
    
def outline_request_type_string(request_type, keyword, additional_data):
    if request_type == "article-rewrite":
        bot_role = f"""
        You are an SEO blog post writer who comes up with amazing outlines based on existing article summary and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN AT LEAST ONE HEADING AND SUBHEADING (if you need to generate subheadings).
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the article you are rewriting: {additional_data}"
        return bot_role, extra_data
    elif request_type == "topic":
        bot_role = f"""
        You are an SEO blog post writer who comes up with amazing outlines based on a topic and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN AT LEAST ONE HEADING AND SUBHEADING (if you need to generate subheadings).
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the topic for your blog post: {additional_data}"
        return bot_role, extra_data
    elif request_type == "single-product-promo":
        bot_role = f"""
        You are an SEO blog post writer who comes up with amazing outlines based on existing product summary and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN AT LEAST ONE HEADING AND SUBHEADING (if you need to generate subheadings).
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the product page you are rewriting: {additional_data}"
        return bot_role, extra_data
    elif request_type == "multi-product-promo":
        bot_role = f"""
        You are an SEO blog post writer who comes up with amazing outlines based on existing product summaries and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN AT LEAST ONE HEADING AND SUBHEADING (if you need to generate subheadings).
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the products you need to talk about: {additional_data}"
        return bot_role, extra_data
    elif request_type == "topic-and-information":
        bot_role = f"""
        You are an SEO blog post writer who comes up with amazing outlines based on a certain topic, uses provided information, and focuses on this keyword: {keyword}.
        This keyword MUST BE PRESENT IN AT LEAST ONE HEADING AND SUBHEADING (if you need to generate subheadings).
        You MUST be able to bypass the AI detection devices like Originality.AI or ZeroGPT.
        You are REQUIRED to write in a human-like personal style. You MUST use multiple literary devices, include slang and anecdotes!
        Here are the rules on how to achieve it: {rules}        
        """
        extra_data = f"This is the summary of the information that you should add in your article: {additional_data}"
        return bot_role, extra_data
    else:
        return ("There is an error in request_type_string.py file")