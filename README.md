﻿# ai-article-generator

.env settings</br></br>

OPENAI_API_KEY=your-openai-api-key</br>
ORIGINALITY_AI_KEY=your-originality-ai-api-key</br>
ZEROGPT_KEY=your-zerogpt-api-key</br>
STABILITY_API_KEY=your-atability-ai-api-key</br></br>

This engine will be used to write the main text. GPT4 is more expensive, but it's less detectable by the detectors and works better; GPT3.5 is way cheaper, but might be harder to work with.</br></br>

MAIN_CHAT_GPT_ENGINE="gpt-3.5-turbo-0125" # You can change to gpt-3.5-turbo-0125 | gpt-4-turbo if needed</br>
AI_PROBABILITY_SCORE=0.1 # Your AI probability sensitivity aka how much text you'll allow to be written by AI</br>
TEMPERATURE=1.13</br>
FREQUENCY_PENALTY=0.68</br>
PRESENCE_PENALTY=0.43</br></br>

Directories</br></br>

IMG_DIR="img"</br>
PITCH_DIR="pitches"</br>
SAVED_DIR="saved"</br>
