# ai-article-generator

.env settings
OPENAI_API_KEY="your-openai-api-key"
ORIGINALITY_AI_KEY="your-originality-ai-api-key"
ZEROGPT_KEY="your-zerogpt-api-key"
STABILITY_API_KEY="your-atability-ai-api-key"

# This engine will be used to write the main text. GPT4 is more expensive, but it's less detectable by the detectors and works better; GPT3.5 is way cheaper, but might be harder to work with.
MAIN_CHAT_GPT_ENGINE="gpt-3.5-turbo-0125" # You can change to gpt-3.5-turbo-0125 | gpt-4-turbo if needed
AI_PROBABILITY_SCORE=0.1 # Your AI probability sensitivity aka how much text you'll allow to be written by AI
TEMPERATURE=1.13
FREQUENCY_PENALTY=0.68
PRESENCE_PENALTY=0.43

# Directories
IMG_DIR="img"
PITCH_DIR="pitches"
SAVED_DIR="saved"