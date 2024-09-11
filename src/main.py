from src.openai.openai_client import OpenAIClient
from src.interaction.intent_recognition import IntentRecognition

def main():
    print("Alfred at your service, Master Wayne. How can I assist you today?")
    openai_client = OpenAIClient()
    intent_recognition = IntentRecognition()

    while True:
        prompt = input("\nYour request: ")
        if prompt.lower() == 'exit':
            print("Goodbye, Master Wayne.")
            break

        # Get the response directly (no need to unpack intent and response)
        openai_response = intent_recognition.recognize_intent(prompt)
        print(f"\nAlfred: {openai_response}")

if __name__ == "__main__":
    main()
