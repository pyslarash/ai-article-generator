from .post_outline import post_outline_article_rewrite, post_outline_topic, post_outline_single_product_promo, post_outline_multiple_products_promo, post_outline_topic_and_info
from .components.voice_type import prompt_voice_type
from .components.post_type import prompt_post_type


def yn_to_tf(question):
    while True:
        answer = input(question + " (Y/N): ").upper()
        if answer == "Y":
            return True
        elif answer == "N":
            return False
        else:
            print("Invalid input. Please enter either Y or N.")

def get_word_count():
    return int(input("Enter number of words needed for this article: "))

def get_wordpress_details():
    if yn_to_tf("Will you need to upload this post to the Wordpress website?"):
        domain = input("Enter the domain name (e.g., example.com): ")
        login = input("Enter the login: ")
        password = input("Enter the password: ")
        return domain, login, password
    else:
        return None, None, None

def select_ai_check():
    if yn_to_tf("Do you need to run an AI check?"):
        print("What AI checking services do you need to use?")
        print("1. ZeroGPT")
        print("2. Originality.ai")
        print("3. Both")
        return int(input("Enter the number corresponding to your choice: "))
    else:
        return None

def select_post_type():
    print("What type of post do you need to create? Choose a number:")
    print("1. I want to rewrite a post from an existing URL.")
    print("2. I have an idea for a post.")
    print("3. I want to promote a single product.")
    print("4. I want to promote multiple products.")
    print("5. I have a topic for a post and want to add some links for reference.")
    return int(input("Enter the number corresponding to your choice: "))

def save_to_file():
    if yn_to_tf("Do you want to save the article to a file?"):
        file_name = input("Enter the file name (without extension): ")
        return file_name
    else:
        return None
    
def generate_pitch():
    if yn_to_tf("Would you like to write a pitch?"):
        file_name = input("Enter the file name (without extension): ")
        return file_name
    else:
        return None
    
def generate_images():
    if yn_to_tf("Would you like to generate image(s) for your post?"):
        file_name = input("Enter the file name (without extension): ")
        num_img = int(input("How many images do you need? "))
        return file_name, num_img
    else:
        return None, None

# Main input function
def user_input():
    words = get_word_count()
    hard_limit = yn_to_tf("Is it a hard limit (do you need less than this amount)?")
    cover_image, num_img = generate_images()
    pitch = generate_pitch()
    ai_check_choice = select_ai_check()    
    wordpress_domain, wordpress_login, wordpress_password = get_wordpress_details()
    file_name = save_to_file()
    
    post_type_num = select_post_type()
    if post_type_num == 1:
        url = input("Provide the URL of an article: ")
        keyword = input("Provide the focus keyword: ")
        meaning = prompt_post_type()
        voice = prompt_voice_type()
        request_type, outline_json, summary, unedited_outline = post_outline_article_rewrite(url, words, keyword, meaning, voice)
    elif post_type_num == 2:
        topic = input("Provide the topic of the article: ")
        keyword = input("Provide the focus keyword: ")
        meaning = prompt_post_type()
        voice = prompt_voice_type()
        request_type, outline_json, topic, unedited_outline = post_outline_topic(topic, words, keyword, meaning, voice)
    elif post_type_num == 3:
        url = input("Provide the URL of a product: ")
        keyword = input("Provide the focus keyword: ")
        meaning = prompt_post_type()
        voice = prompt_voice_type()
        request_type, outline_json, summary, unedited_outline = post_outline_single_product_promo(url, words, keyword, meaning, voice)
    elif post_type_num == 4:
        num_of_products = int(input("How many products you would like to promote in your post: "))
        urls = []
        for i in range(num_of_products):
            link = input(f"Provide the URL of product {i+1}: ")
            urls.append(link)
        keyword = input("Provide the focus keyword: ")
        meaning = prompt_post_type()
        voice = prompt_voice_type()
        request_type, outline_json, summary_string, unedited_outline = post_outline_multiple_products_promo(urls, words, keyword, meaning, voice)
    elif post_type_num == 5:
        topic = input("Provide the topic of the article: ")
        num_of_products = int(input("How many links would you like to add for reference in your post: "))
        urls = []
        for i in range(num_of_products):
            link = input(f"Provide the URL of reference {i+1}: ")
            urls.append(link)
        keyword = input("Provide the focus keyword: ")
        meaning = prompt_post_type()
        voice = prompt_voice_type()
        request_type, outline_json, summary_string, unedited_outline = post_outline_topic_and_info(topic, urls, words, keyword, meaning, voice)

    if request_type == "article-rewrite" or request_type == "single-product-promo":
        return request_type, words, keyword, outline_json, unedited_outline, summary, meaning, voice, ai_check_choice, hard_limit, cover_image, num_img, pitch, wordpress_domain, wordpress_login, wordpress_password, file_name
    elif request_type == "topic":
        return request_type, words, keyword, outline_json, unedited_outline, topic, meaning, voice, ai_check_choice, hard_limit, cover_image, num_img, pitch, wordpress_domain, wordpress_login, wordpress_password, file_name
    elif request_type == "multi-product-promo":
        return request_type, words, keyword, outline_json, unedited_outline, summary_string, meaning, voice, ai_check_choice, hard_limit, cover_image, num_img, pitch, wordpress_domain, wordpress_login, wordpress_password, file_name
    elif request_type == "topic-and-information":
        return request_type, words, keyword, outline_json, unedited_outline, summary_string, meaning, voice, ai_check_choice, hard_limit, cover_image, num_img, pitch, wordpress_domain, wordpress_login, wordpress_password, file_name
    else:
        return "Something went wrong!"