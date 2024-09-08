import openai
import subprocess
from config.config import openai_api_key

# Set your OpenAI API key
openai.api_key = openai_api_key

# Function to send a prompt to OpenAI and get a terminal command
def ai_assistant(prompt):
    prompt = f"You're an AI Butler like Alfred from Batman {prompt}."

    # Get response from OpenAI
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're really helpful"},
            {"role": "user", "content": prompt}
        ]
    )
    advice = response.choices[0].message.content
    return advice

# Function to execute the terminal command
def execute_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"Command Output:\n{result.stdout}")
    except Exception as e:
        print(f"Error executing command: {e}")

def main():
    while True:
        prompt = input("What task would you like to perform (type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        advice = ai_assistant(prompt)
        print(f"\nGenerated Advice: {advice}")

        # Ask the user if they want to execute the command
        confirm = input("Do you want to execute this advice as a terminal command? (y/n): ").lower()
        if confirm == 'y':
            execute_command(advice)
        else:
            print("Command not executed.")

if __name__ == "__main__":
    main()
