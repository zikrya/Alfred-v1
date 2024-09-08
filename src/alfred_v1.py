import openai
import subprocess
import os
from config.config import openai_api_key

openai.api_key = openai_api_key

def ai_assistant(prompt):
    refined_prompt = f"As Alfred, the trusted butler of Batman, provide a polite response to the following command, and then generate the exact terminal command to perform the task without any further explanation: {prompt}"

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're Alfred, Batman's butler. Always be polite and helpful, and generate the correct terminal command for any task given to you."},
            {"role": "user", "content": refined_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def extract_command(response):
    lines = response.splitlines()

    filtered_lines = [line for line in lines if not line.startswith("```")]

    for line in filtered_lines[::-1]:
        if line.strip():
            return line.strip()
    return None

def execute_command(command):
    try:
        print(f"Executing Command: {command}")
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"Command Output:\n{result.stdout}")
    except Exception as e:
        print(f"Error executing command: {e}")

# Function to process the command and handle conversational touch
def process_command(prompt):
    # Get a conversational response and the terminal command from Alfred
    alfred_response = ai_assistant(prompt)
    print(f"\nAlfred: {alfred_response}")

    # Extract the bash command and execute it
    command = extract_command(alfred_response)
    if command:
        print(f"Extracted Command: {command}")
        execute_command(command)
    else:
        print("No valid command found in the response.")

def main():
    print("Alfred at your service, Master Wayne. How can I assist you today?")
    while True:
        prompt = input("\nYour request: ")
        if prompt.lower() == 'exit':
            print("Goodbye, Master Wayne.")
            break

        process_command(prompt)

if __name__ == "__main__":
    main()
