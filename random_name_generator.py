import os
import random
import string

# Directory where the files are stored
DIRECTORY = "extracted_text"

def generate_random_name(length=64):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate a random name of the specified length
    random_name = ''.join(random.choice(characters) for _ in range(length))

    return random_name

def check_existing_names():
    existing_names = set()
    for filename in os.listdir(DIRECTORY):
        if filename.endswith(".txt"):
            existing_names.add(filename)
    return existing_names

def generate_unique_name(length=64):
    existing_names = check_existing_names()
    while True:
        random_name = generate_random_name(length)
        if random_name not in existing_names:
            return random_name