from .user_input import user_input
from .article_writer import article_writer, full_json_article
import sys
import json
sys.path.append('components')
from .components.word_count import count_words_in_article
from .components.minimize_article import fit_to_word_limit
from .components.save_file import save_json_to_txt
from .components.gpt_global_prompts import save_pitch_to_file, cover_image_generator
from .components.wordpress_upload import check_wordpress_info
from .components.zerogpt_check import zerogpt_check
from .components.originality_check import originality_check

def article_mode():
    try:
        print("Setting up the type of post to generate...")
        (request_type, words, keyword, json_data, unedited_outline, additional_data, meaning, voice, ai_check_choice,
         hard_limit, cover_image, num_img, pitch, wordpress_domain, wordpress_login, wordpress_password, file_name) = user_input()
        
        main_content, summary = article_writer(json_data, keyword, request_type, additional_data, meaning, voice)
        final_article = full_json_article(main_content, summary, words, keyword, voice, meaning, unedited_outline)
        
        # Ensure final_article is a JSON string before passing to fit_to_word_limit
        final_article_json = json.dumps(final_article) if isinstance(final_article, dict) else final_article
        
        word_count = count_words_in_article(final_article_json)  # Ensure it's loaded as a dict to count words
        print(f"Initial word count is: {word_count}")

        if hard_limit:  # Checking if hard limit is true
            if word_count > int(words):  # Here 'words' is assumed to be the numerical limit
                print(f"Current word count {word_count} exceeds the limit of {words}. Starting reduction process...")
                final_article_json = fit_to_word_limit(final_article_json, keyword, request_type, additional_data, meaning, voice, int(words))
                new_word_count = int(count_words_in_article(json.loads(final_article_json)))
                print(f"New word count after shrinking is {new_word_count}.")
                if new_word_count > int(words):
                    print("Warning: Unable to reduce word count to below the hard limit.")
                else:
                    print("Text successfully shrunk to fit within the hard limit.")
            else:
                print("No need to shrink text.")
                
        if file_name:  # Check if file_name is provided
            save_json_to_txt(final_article_json, file_name)
            print(f"JSON data saved to {file_name}.txt successfully.")
            
        if cover_image:  # Check if file_name is provided
            cover_image_generator(summary, num_img, cover_image)
            print(f"Cover image(s) saved successfully to {cover_image}.png.")
            
        if pitch:
            save_pitch_to_file(summary, pitch)
            print(f"Pitch saved successfully to {pitch}.txt.")
            
        if ai_check_choice:
            if ai_check_choice == 3:
                zero_gpt_result = zerogpt_check(final_article_json)
                originality_ai_result = originality_check(final_article_json)
                if zero_gpt_result and originality_ai_result:
                    print("BOTH ZeroGPT check and Originality.ai check PASSED.")
                elif zero_gpt_result:
                    print("ZeroGPT check PASSED; Originality.ai check FAILED.")
                elif originality_ai_result:
                    print("ZeroGPT check FAILED; Originality.ai check PASSED.")
                else:
                    print("Both ZeroGPT check and Originality.ai checks failed.")
            elif ai_check_choice == 2:
                originality_ai_result = originality_check(final_article_json)
                if originality_ai_result:
                    print("Originality.ai check PASSED")
                else:
                    print("Originality.ai check FAILED")
            elif ai_check_choice == 1:
                zero_gpt_result = zerogpt_check(final_article_json)
                if zero_gpt_result:
                    print("ZeroGPT check PASSED")
                else:
                    print("ZeroGPT check FAILED")
            
        check_wordpress_info(wordpress_domain, wordpress_login, wordpress_password, final_article_json)
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def main():
    article_mode()

if __name__ == "__main__":
    main()