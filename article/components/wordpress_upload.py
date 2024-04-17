import requests
import json

def create_post(domain_name, login, password, post_data):
    url = f"https://{domain_name}/wp-json/wp/v2/posts"
    headers = {'Content-Type': 'application/json'}
    auth = (login, password)
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(post_data))
    return response.json()

def wrap_headings(text, level):
    if level == 2:
        return f"<h2>{text}</h2>"
    elif level == 3:
        return f"<h3>{text}</h3>"

def wrap_paragraphs(text):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    wrapped_paragraphs = [f"<p>{paragraph}</p>" for paragraph in paragraphs]
    return "".join(wrapped_paragraphs)

def format_post(post):
    if isinstance(post, str):
        post = json.loads(post)
    formatted_post = {}

    formatted_post["title"] = post["article_title"]
    formatted_post["content"] = ""

    formatted_post["content"] += wrap_paragraphs(post["intro"])  # Wrap each paragraph of the intro with <p> tags

    for section in post["body"]:
        formatted_post["content"] += wrap_headings(section["heading_title"], 2)
        formatted_post["content"] += wrap_paragraphs(section["heading_text"])

        if "subheadings" in section:
            for subheading in section["subheadings"]:
                formatted_post["content"] += wrap_headings(subheading["subheading_title"], 3)
                formatted_post["content"] += wrap_paragraphs(subheading["subheading_text"])

    formatted_post["content"] += wrap_headings(post["conclusion_title"], 2)
    formatted_post["content"] += wrap_paragraphs(post["conclusion"])

    return formatted_post

def wordpress(domain_name, login, password, post_data):
    formatted_post_data = format_post(post_data)
    response = create_post(domain_name, login, password, formatted_post_data)
    return response

def check_wordpress_info(domain, login, password, post_data):
    missing_info = []
    if not domain:
        missing_info.append("domain")
    if not login:
        missing_info.append("login")
    if not password:
        missing_info.append("password")

    # Check if all are missing
    if len(missing_info) == 3:
        return  # Do not return anything if all are None

    # Check if any info is missing
    if missing_info:
        print("Some Wordpress information is missing:", ", ".join(missing_info))
    else:
        wordpress(domain, login, password, post_data)
        print(f"Check Posts section on your Wordpress website...")