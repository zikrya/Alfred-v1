from src.openai.openai_client import OpenAIClient
from src.interaction.intent_recognition import IntentRecognition
from src.voice.tts import speak_response  # Import the TTS function

def main():
    print("Alfred at your service, Master Zack. How can I assist you today?")
    openai_client = OpenAIClient()
    intent_recognition = IntentRecognition()

    while True:
        prompt = input("\nYour request: ")
        if prompt.lower() == 'exit':
            print("Goodbye, Master Zack.")
            break

        openai_response = intent_recognition.recognize_intent(prompt)
        print(f"\nAlfred: {openai_response}")

        speak_response(openai_response)

if __name__ == "__main__":
    main()
