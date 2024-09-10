from src.openai.openai_client import OpenAIClient


def main():
    print("Alfred at your service, Master Wayne. How can I assist you today?")
    openai_client = OpenAIClient()

    while True:
        prompt = input("\nYour request: ")
        if prompt.lower() == 'exit':
            print("Goodbye, Master Wayne.")
            break

        alfred_response = openai_client.ai_assistant(prompt)
        print(f"\nAlfred: {alfred_response}")

if __name__ == "__main__":
    main()
