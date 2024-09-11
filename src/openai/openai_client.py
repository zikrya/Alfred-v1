import openai
from config.config import openai_api_key
from src.system_commands.folder_file_operations import create_folder, create_file, list_files_and_folders, search_for_file, search_for_folder, read_file_contents
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
            "For commands that involve system actions (like creating, deleting, searching for files or folders), interpret the command clearly and provide the required action. "
            "For general questions or non-actionable requests, provide helpful and conversational responses. "
            "Always maintain the tone of Alfred—polite, helpful, and slightly witty."
        )

        # Define available functions for function calling
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
                "name": "list_files_and_folders",
                "description": "List all files and folders in a specified directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "The path to list the contents of."}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "search_for_file",
                "description": "Search for a file in the system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "The name of the file to search for."},
                        "search_path": {"type": "string", "description": "The path to start searching in."}
                    },
                    "required": ["filename"]
                }
            },
            {
                "name": "search_for_folder",
                "description": "Search for a folder in the system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "foldername": {"type": "string", "description": "The name of the folder to search for."},
                        "search_path": {"type": "string", "description": "The path to start searching in."}
                    },
                    "required": ["foldername"]
                }
            },
            {
                "name": "read_file_contents",
                "description": "Read the contents of a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "The full path of the file to read."}
                    },
                    "required": ["filepath"]
                }
            }
        ]

        # Send the request to OpenAI with function calling
        response = self.client.chat.completions.create(
            model="gpt-4",
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
            elif function_name == "list_files_and_folders":
                return list_files_and_folders(arguments.get("path", "."))
            elif function_name == "search_for_file":
                return search_for_file(arguments["filename"], arguments.get("search_path", "."))
            elif function_name == "search_for_folder":
                return search_for_folder(arguments["foldername"])
            elif function_name == "read_file_contents":
                return read_file_contents(arguments["filepath"])

        if hasattr(message, "content") and message.content:
            return message.content

        return "I couldn't quite catch that, Master Zack. Could you rephrase?"
