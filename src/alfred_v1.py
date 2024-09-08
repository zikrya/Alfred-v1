import openai
import subprocess
import os
from config.config import openai_api_key

openai.api_key = openai_api_key

def ai_assistant(prompt):
    refined_prompt = f"As Alfred, Batman's trusted butler, politely respond to the user's input. If it is a command, provide the exact terminal command to perform it. If it is a general question, simply answer without generating a terminal command."

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're Alfred, Batman's butler. Always be polite and helpful. For questions, provide a conversational answer. For tasks, provide the correct terminal command."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def extract_command(response):
    lines = response.splitlines()

    filtered_lines = [line for line in lines if not line.startswith("```")]

    for line in filtered_lines[::-1]:
        if line.strip():
            if any(cmd in line for cmd in ["mkdir", "cd", "rm", "echo", "ls", "touch", "open"]):
                return line.strip()
    return None

def execute_command(command):
    try:
        print(f"Executing Command: {command}")
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"Command Output:\n{result.stdout}")
    except Exception as e:
        print(f"Error executing command: {e}")

def process_command(prompt):
    alfred_response = ai_assistant(prompt)
    print(f"\nAlfred: {alfred_response}")

    command = extract_command(alfred_response)

    if command:
        print(f"Extracted Command: {command}")
        execute_command(command)
    else:
        print("No command to execute. This was likely a general question.")

def main():
    print("Alfred at your service, Master Zack. How can I assist you today?")
    while True:
        prompt = input("\nYour request: ")
        if prompt.lower() == 'exit':
            print("Goodbye, Master Zack.")
            break

        process_command(prompt)

if __name__ == "__main__":
    main()
