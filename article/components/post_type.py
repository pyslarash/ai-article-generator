def get_post_meaning(post_type):
    if post_type == "informational":
        return "informational (meaning you need to cover the informational aspect of the topic)"
    elif post_type == "how-to":
        return "how-to (meaning you need to explain how to do a certain thing preferably step-by-step)"
    elif post_type == "expanded":
        return "expanded (meaning you will need to explain a certain topic and then explain what or how to do with this topic)"
    elif post_type == "list-post":
        return "list (meaning you will list and discuss multiple things like products, services, etc. you will need to list them in your headings)"
    else:
        return "Post type not recognized."
    
def choose_post_type(post_type_num):
    if post_type_num == 1:
        post_type = "informational"
    elif post_type_num == 2:
        post_type = "how-to"
    elif post_type_num == 3:
        post_type = "expanded"
    elif post_type_num == 4:
        post_type = "list-post"
    else:
        post_type = None
        
    type_description = get_post_meaning(post_type)
    
    return type_description

def prompt_post_type():
    print("Select a post type:")
    print("1. Informational")
    print("2. How-to")
    print("3. Expanded")
    print("4. List Post")

    post_type_num = int(input("Enter the number corresponding to the post type: "))
    description = choose_post_type(post_type_num)
    return description