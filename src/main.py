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

        # Recognize intent and generate both action and response
        intent, openai_response = intent_recognition.recognize_intent(prompt)  # Unpack both intent and response
        action = intent_recognition.generate_action(intent, prompt)

        print(f"\nAlfred: {action}")

if __name__ == "__main__":
    main()


