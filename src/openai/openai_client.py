import openai
from config.config import openai_api_key
from src.system_commands.folder_file_operations import create_folder, create_file
import json

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai.OpenAI(api_key=openai_api_key)
        return cls._instance

    def ai_assistant(self, prompt):
        refined_prompt = (
            f"As Alfred, Batman's trusted butler, you must always respond politely and respectfully to the user's input. "
            "For commands that involve system actions (like creating, deleting, or searching for files), interpret the command clearly and provide the required action. "
            "For general questions or non-actionable requests, provide helpful and conversational responses. "
            "Always maintain the tone of Alfred—polite, helpful, and slightly witty."
        )

        # Define the available functions for function calling
        functions = [
            {
                "name": "create_folder",
                "description": "Create a folder at the given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "folder_name": {"type": "string", "description": "The name of the folder to create."},
                        "path": {"type": "string", "description": "The path where the folder should be created."}
                    },
                    "required": ["folder_name"]
                }
            },
            {
                "name": "create_file",
                "description": "Create a file at the given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {"type": "string", "description": "The name of the file to create."},
                        "path": {"type": "string", "description": "The path where the file should be created."}
                    },
                    "required": ["file_name"]
                }
            }
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": refined_prompt},
                {"role": "user", "content": prompt}
            ],
            functions=functions,
            function_call="auto"
        )


        message = response.choices[0].message

        if message.function_call:
            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)

            if function_name == "create_folder":
                return create_folder(arguments["folder_name"], arguments.get("path", "."))
            elif function_name == "create_file":
                return create_file(arguments["file_name"], arguments.get("path", "."))

        if hasattr(message, "content") and message.content:
            return message.content

        return "I couldn't quite catch that, Master Wayne. Could you rephrase?"
