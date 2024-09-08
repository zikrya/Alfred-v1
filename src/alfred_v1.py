import openai
from config.config import openai_api_key

# Set your OpenAI API key
openai.api_key = openai_api_key

def ai_assistant(prompt):
    prompt = f"You're an AI Buttler like Alfred from Batman {prompt}."

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're really helpful"},
            {"role": "user", "content": prompt}
        ]
    )
    advice = response.choices[0].message.content
    return advice


def main():
    prompt = input("Test out alfred")
    advice = ai_assistant(prompt)
    print(f"\n{advice}")

if __name__ == "__main__":
    main()