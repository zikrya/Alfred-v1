import openai
import subprocess
from config.config import openai_api_key

# Set your OpenAI API key
openai.api_key = openai_api_key

# Function to send a prompt to OpenAI and get the terminal command
def ai_assistant(prompt):
    # Refine the prompt to instruct OpenAI to ONLY return the command without explanation
    refined_prompt = f"Generate only the exact terminal command for macOS to perform the following action without any explanation: {prompt}"

    # Get response from OpenAI
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a macOS terminal assistant. Only return valid commands without explanations."},
            {"role": "user", "content": refined_prompt}
        ]
    )
    # Return the response which should now only be a terminal command
    return response.choices[0].message.content.strip()

# Function to execute the terminal command
def execute_command(command):
    try:
        # Run the command in the terminal
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"Command Output:\n{result.stdout}")
    except Exception as e:
        print(f"Error executing command: {e}")

def main():
    while True:
        prompt = input("What task would you like to perform (type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        command = ai_assistant(prompt)
        print(f"Generated Command: {command}")

        # Execute the generated command directly
        execute_command(command)

if __name__ == "__main__":
    main()
