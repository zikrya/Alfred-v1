import openai
import subprocess
import os
from config.config import openai_api_key

openai.api_key = openai_api_key

def ai_assistant(prompt):
    refined_prompt = f"Generate only the exact terminal command for macOS to perform the following action without any explanation: {prompt}"

    # Get response from OpenAI
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a macOS terminal assistant. Only return valid commands without explanations."},
            {"role": "user", "content": refined_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def list_folders_in_directory(directory):
    try:
        folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        if not folders:
            print(f"No folders found in {directory}")
        else:
            print(f"Folders in {directory}:")
            for folder in folders:
                print(f"- {folder}")
    except Exception as e:
        print(f"Error accessing {directory}: {e}")

def execute_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"Command Output:\n{result.stdout}")
    except Exception as e:
        print(f"Error executing command: {e}")

def process_command(prompt):
    if "list folders" in prompt.lower() and "desktop" in prompt.lower():
        list_folders_in_directory(os.path.expanduser("~/Desktop"))
    else:
        command = ai_assistant(prompt)
        print(f"Generated Command: {command}")
        execute_command(command)

def main():
    while True:
        prompt = input("What task would you like to perform (type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break

        process_command(prompt)

if __name__ == "__main__":
    main()
