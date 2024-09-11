import openai
import os
from config.config import openai_api_key

openai.api_key = openai_api_key

def speak_response(text):
    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=text
        )

        audio_file = "response.mp3"
        response.stream_to_file(audio_file)

        os.system(f"afplay {audio_file}")
    except Exception as e:
        print(f"Error generating TTS: {e}")
