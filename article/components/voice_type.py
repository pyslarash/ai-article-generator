def choose_voice_type(voice_type_num):
    if voice_type_num == 1:
        voice_type = "business"
    elif voice_type_num == 2:
        voice_type = "promotional"
    elif voice_type_num == 3:
        voice_type = "friendly"
    elif voice_type_num == 4:
        voice_type = "informational"
    else:
        voice_type = None
    
    return voice_type

def prompt_voice_type():
    print("Select a voice type:")
    print("1. Business")
    print("2. Promotional")
    print("3. Friendly")
    print("4. Informational")

    voice_type_num = int(input("Enter the number corresponding to the post type: "))
    v_type = choose_voice_type(voice_type_num)
    return v_type